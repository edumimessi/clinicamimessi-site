(function(){
  if (localStorage.getItem('cm_cookies_ok')) return;
  var bar = document.createElement('div');
  bar.id = 'cm-cookie-bar';
  bar.style.cssText = 'position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#0f2744;color:#fff;padding:14px 20px;display:flex;gap:16px;align-items:center;justify-content:center;flex-wrap:wrap;font-size:0.85rem;font-family:Inter,sans-serif;box-shadow:0 -4px 20px rgba(0,0,0,0.15)';
  var isSub = location.pathname.split('/').length > 2 && location.pathname.indexOf('.html') > -1 && (location.pathname.indexOf('/blog/') > -1 || location.pathname.indexOf('/especialidades/') > -1);
  var pol = (isSub ? '../' : '') + 'politica-de-privacidade.html';
  bar.innerHTML = '<span>Usamos cookies para melhorar sua experiência e analisar o uso do site. Saiba mais na nossa <a href="' + pol + '" style="color:#9ee2e2;text-decoration:underline">Política de Privacidade</a>.</span><button id="cm-cookie-ok" style="background:#1a6e6e;color:#fff;border:none;border-radius:50px;padding:8px 24px;font-weight:600;cursor:pointer;font-size:0.85rem">Entendi</button>';
  document.body.appendChild(bar);
  document.getElementById('cm-cookie-ok').addEventListener('click', function(){
    localStorage.setItem('cm_cookies_ok', '1');
    bar.remove();
  });
})();
