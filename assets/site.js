/* ============================================================
   Leitor de documentos — busca os .md reais do repositório
   e os renderiza no estilo do site. Reescreve os links internos
   para navegar dentro do próprio leitor.
   ============================================================ */
(function () {
  'use strict';

  var REPO = 'saulofilho/prompt-engineering-ptbr';
  var BRANCH = 'main';
  var DEFAULT = 'README.md';

  var contentEl = document.getElementById('content');
  var crumbEl = document.getElementById('crumb');
  var footEl = document.getElementById('footlinks');
  var ghEl = document.getElementById('ghlink');

  // ---- caminho pedido (?p=...) ----
  var params = new URLSearchParams(location.search);
  var path = params.get('p') || DEFAULT;

  // Só aceita caminho relativo seguro dentro do repo.
  function safePath(p) {
    if (!p) return null;
    if (/^(https?:)?\/\//i.test(p)) return null;   // sem URLs absolutas
    if (p.charAt(0) === '/') p = p.replace(/^\/+/, '');
    if (p.indexOf('..') !== -1) return null;        // sem subir diretório
    if (!/^[A-Za-z0-9._/\-]+$/.test(p)) return null; // só caracteres de caminho
    return p;
  }

  path = safePath(path);

  if (!path) {
    showError('caminho de documento inválido.');
    return;
  }

  // ---- resolve um href relativo a partir do caminho do doc atual ----
  function resolveFrom(base, href) {
    try {
      var b = new URL(base, 'https://repo.local/');
      var u = new URL(href, b);
      return u.pathname.replace(/^\/+/, '') + (u.hash || '');
    } catch (e) {
      return href;
    }
  }

  function titleFromPath(p) {
    var name = p.split('/').pop();
    return name;
  }

  // ---- busca e renderiza ----
  fetch(path, { headers: { 'Accept': 'text/plain' } })
    .then(function (r) {
      if (!r.ok) throw new Error(r.status + '');
      return r.text();
    })
    .then(function (md) {
      render(md);
    })
    .catch(function (err) {
      if (err && err.message === '404') {
        showError('documento não encontrado: <code>' + escapeHtml(path) + '</code>');
      } else {
        showError('não foi possível carregar <code>' + escapeHtml(path) + '</code> (' +
          escapeHtml(String(err && err.message || err)) + ').');
      }
    });

  function render(md) {
    if (window.marked && typeof window.marked.setOptions === 'function') {
      window.marked.setOptions({ gfm: true, breaks: false, headerIds: true, mangle: false });
    }
    var html = window.marked ? window.marked.parse(md) : ('<pre>' + escapeHtml(md) + '</pre>');
    contentEl.innerHTML = html;

    rewriteLinks();
    rewriteImages();

    // título e migalha
    var t = titleFromPath(path);
    crumbEl.textContent = path;
    document.title = t + ' · prompt preciso';
    ghEl.href = 'https://github.com/' + REPO + '/blob/' + BRANCH + '/' + path;
    footEl.hidden = false;

    // rola para a âncora, se houver
    if (location.hash) {
      var target = document.getElementById(location.hash.slice(1));
      if (target) target.scrollIntoView();
    }
  }

  function rewriteLinks() {
    var links = contentEl.querySelectorAll('a[href]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var href = a.getAttribute('href');
      if (!href) continue;

      // âncora na própria página → mantém
      if (href.charAt(0) === '#') continue;

      // link absoluto (http/mailto/etc.) → abre em nova aba
      if (/^(https?:)?\/\//i.test(href) || /^mailto:/i.test(href)) {
        a.setAttribute('target', '_blank');
        a.setAttribute('rel', 'noopener');
        continue;
      }

      var resolved = resolveFrom(path, href);
      var bare = resolved.split('#')[0];

      if (/\.md$/i.test(bare)) {
        // outro documento → navega dentro do leitor
        a.setAttribute('href', 'leitor.html?p=' + encodeURIComponent(bare));
      } else {
        // arquivo não-md do repo (LICENSE, .py, .json…) → github
        a.setAttribute('href', 'https://github.com/' + REPO + '/blob/' + BRANCH + '/' + resolved);
        a.setAttribute('target', '_blank');
        a.setAttribute('rel', 'noopener');
      }
    }
  }

  function rewriteImages() {
    var imgs = contentEl.querySelectorAll('img[src]');
    for (var i = 0; i < imgs.length; i++) {
      var img = imgs[i];
      var src = img.getAttribute('src');
      if (!src || /^(https?:)?\/\//i.test(src) || src.indexOf('data:') === 0) continue;
      // resolve relativo ao doc e serve a partir da raiz do site
      img.setAttribute('src', resolveFrom(path, src).split('#')[0]);
      img.setAttribute('loading', 'lazy');
    }
  }

  function showError(msgHtml) {
    contentEl.innerHTML =
      '<h1>ops.</h1><p>' + msgHtml + '</p>' +
      '<p><a href="./#docs">← voltar aos documentos</a> · ' +
      '<a href="https://github.com/' + REPO + '" target="_blank" rel="noopener">abrir o repositório ↗</a></p>';
    if (crumbEl) crumbEl.textContent = path || '';
    document.title = 'documento não encontrado · prompt preciso';
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
})();
