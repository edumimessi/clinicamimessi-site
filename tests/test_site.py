"""Static regression checks. Run: python -m unittest discover -s tests -v"""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class SiteTests(unittest.TestCase):
    def test_documents_have_one_body_and_unique_ids(self):
        for path in ROOT.rglob('*.html'):
            source = path.read_text(encoding='utf-8')
            page = Page(source)
            with self.subTest(page=path.relative_to(ROOT)):
                self.assertEqual(sum(tag == 'body' for tag, _ in page.tags), 1)
                self.assertFalse(source.split('</html>', 1)[1].strip())
                ids = Counter(a['id'] for _, a in page.tags if 'id' in a)
                self.assertFalse([key for key, count in ids.items() if count > 1])

    def test_local_resources_exist(self):
        for path in ROOT.rglob('*.html'):
            for tag, attrs in Page(path.read_text(encoding='utf-8')).tags:
                if tag not in ('a', 'script', 'link', 'img', 'source'):
                    continue
                values = [attrs[key] for key in ('href', 'src') if key in attrs]
                values += [part.strip().split()[0] for part in attrs.get('srcset', '').split(',') if part.strip()]
                for value in values:
                    url = urlsplit(value)
                    if url.scheme or url.netloc or not url.path:
                        continue
                    target = (ROOT if url.path.startswith('/') else path.parent) / unquote(url.path).lstrip('/')
                    with self.subTest(page=path.relative_to(ROOT), resource=value):
                        self.assertTrue(target.exists(), str(target))

    def test_navigation_has_one_shared_handler(self):
        for path in ROOT.rglob('*.html'):
            source = path.read_text(encoding='utf-8')
            if 'id="navLinks"' not in source:
                continue
            page = Page(source)
            with self.subTest(page=path.relative_to(ROOT)):
                self.assertEqual(sum(tag == 'script' and a.get('src', '').endswith('assets/navigation.js') for tag, a in page.tags), 1)
                self.assertNotIn("getElementById('hamburger').addEventListener", source)
                for tag, attrs in page.tags:
                    if 'dropdown-toggle' in attrs.get('class', '').split():
                        self.assertEqual(tag, 'button')
                        self.assertEqual(attrs.get('aria-expanded'), 'false')
                self.assertIn('vida-e-sentido.html', source.split('id="navLinks"', 1)[1].split('</ul>', 1)[0])

    def test_devotional_entry_points_and_sitemap(self):
        url = 'https://clinicamimessi.com.br/vida-e-sentido.html'
        sitemap = ET.parse(ROOT / 'sitemap.xml')
        urls = [node.text for node in sitemap.findall('.//{*}loc')]
        self.assertEqual(urls.count(url), 1)
        page = Page((ROOT / 'vida-e-sentido.html').read_text(encoding='utf-8'))
        cards = [a for tag, a in page.tags if tag == 'a' and 'trad-card' in a.get('class', '').split()]
        self.assertEqual(len(cards), 8)
        self.assertEqual(len({a['href'] for a in cards}), 8)
        for card in cards:
            self.assertTrue(card['href'].startswith('https://'))
            self.assertEqual(card.get('target'), '_blank')
            self.assertIn('noopener', card.get('rel', '').split())
        for name in ('index.html', 'cartao.html'):
            source = (ROOT / name).read_text(encoding='utf-8')
            self.assertIn('href="vida-e-sentido.html"', source)
            self.assertNotIn('href="https://vidaesentido.com.br"', source)


if __name__ == '__main__':
    unittest.main()
