/* Reader: reading aids for a long, linked page published as an artifact.
   Markup contract: references/reader-page.md. Every feature is a no-op when its markup is absent
   and can be switched with data-reader on <main> ("all -slash", "popover search tabs", ...).
   No window.prompt, alert, confirm or print. Hashes are plain tokens. Storage is not used. */
(function () {
  "use strict";

  /* ---------- Named constants: every timing and threshold lives here ---------- */
  var T = {
    POP_CLOSE_DELAY_MS: 250,      // hover or focus leaves a trigger: close after this delay
    POP_GAP_PX: 6,                // distance between trigger and popover
    POP_EDGE_PX: 8,               // minimum distance to the viewport edge
    POP_MAX_USES: 6,              // sections listed in "Used N times" before "N more"
    POP_TIP_SEP: " · ",      // "Header · body" inside data-tip
    SPY_LINE_RATIO: 0.25,         // reading line, as a share of the viewport height
    NAV_SCROLL_RATIO: 1 / 3,      // active menu item is scrolled to this height of the menu
    BACK_NEAR_PX: 48,             // the back pill hides when you are this close to where you were
    COPIED_MS: 1600,              // "Copied" label time
    LIVE_CLEAR_MS: 4000,          // live region is emptied after this time
    FILTER_DEBOUNCE_MS: 120,      // menu filter typing delay
    SEARCH_MAX_ROWS: 40,          // result rows shown
    SEARCH_LABEL_MAX: 140,        // characters of a definition shown as its label
    SHORT_TIP_MAX: 160,           // longest definition shown in a popover before it is cut
    SMALL_TEXT_RATIO: 0.65,       // rendered width / viewBox width below which the hint shows
    FIT_FILL: 0.95,               // share of the viewer the diagram fills when fitted
    WHEEL_STEP: 1.15,             // viewer zoom per wheel tick
    BUTTON_STEP: 1.25,            // viewer zoom per button or key
    ZOOM_MIN: 0.1,
    ZOOM_MAX: 12,
    ENHANCE_DEBOUNCE_MS: 300,     // after a diagram renders
    ENHANCE_LOAD_MS: 600,         // one more pass after load
    DRAWER_BREAKPOINT_PX: 960     // keep equal to the media query in reader.css
  };
  /* ---------- UI strings: one dictionary per language, picked from the closest [lang] ----------
     "{n}" and "{name}" are filled by say(). data-reader-strings on .reader-root (a JSON object) merges over the pick. */
  var STRINGS = {
    en: {
      back: "↑ Back to where you were",
      returned: "Returned to where you were",
      searchBtnSlash: "Search  ( / or Ctrl+K )",
      searchBtn: "Search  ( Ctrl+K )",
      filter: "Filter contents",
      noMatch: "No section matches.",
      matchOne: "{n} section matches",
      matchMany: "{n} sections match",
      menuBtn: "☰ Contents",
      closeMenu: "Close contents",
      copy: "Copy",
      copied: "Copied",
      copiedLive: "Copied to the clipboard",
      selectedCopy: "Selected, press Ctrl+C",
      selectedLive: "Text selected, press Ctrl+C to copy",
      textToCopy: "Text to copy",
      copyCode: "Copy code",
      copyLink: "Copy link",
      copyLinkTo: "Copy link to {name}",
      scrollTable: "Scrollable table",
      noDefinition: "No definition found",
      usedOne: "Used {n} time",
      usedMany: "Used {n} times",
      thisPage: "this page",
      more: "{n} more",
      goDefinition: "Go to definition",
      openSource: "Open the source ↗",
      searchThisPage: "Search this page",
      search: "Search",
      results: "Results",
      noResult: "No result",
      resultOne: "{n} result",
      resultMany: "{n} results",
      searchPlaceholderId: "Search headings, IDs (for example {example}) and terms",
      searchPlaceholder: "Search headings and terms",
      searchHint: "Enter opens the selected result · arrows move · Esc closes",
      nodeLink: "{text}. Press Enter to go to the definition.",
      figure: "Figure ",
      figureShort: "Figure",
      figures: "Figures",
      figureViewer: "Figure viewer",
      textSmall: "Text is small: expand to read",
      expand: "⤢ Expand",
      openFull: "Open {title} full screen with zoom",
      viewerHint: "wheel or pinch zooms, drag pans, double-click fits",
      zoomIn: "Zoom in",
      zoomOut: "Zoom out",
      fit: "Fit",
      closeViewer: "Close (Esc)"
    },
    pt: {
      back: "↑ Voltar para onde você estava",
      returned: "Voltou para onde você estava",
      searchBtnSlash: "Buscar  ( / ou Ctrl+K )",
      searchBtn: "Buscar  ( Ctrl+K )",
      filter: "Filtrar sumário",
      noMatch: "Nenhuma seção corresponde.",
      matchOne: "{n} seção corresponde",
      matchMany: "{n} seções correspondem",
      menuBtn: "☰ Sumário",
      closeMenu: "Fechar sumário",
      copy: "Copiar",
      copied: "Copiado",
      copiedLive: "Copiado para a área de transferência",
      selectedCopy: "Selecionado, pressione Ctrl+C",
      selectedLive: "Texto selecionado, pressione Ctrl+C para copiar",
      textToCopy: "Texto para copiar",
      copyCode: "Copiar código",
      copyLink: "Copiar link",
      copyLinkTo: "Copiar link para {name}",
      scrollTable: "Tabela com rolagem",
      noDefinition: "Nenhuma definição encontrada",
      usedOne: "Usado {n} vez",
      usedMany: "Usado {n} vezes",
      thisPage: "esta página",
      more: "mais {n}",
      goDefinition: "Ir para a definição",
      openSource: "Abrir a fonte ↗",
      searchThisPage: "Buscar nesta página",
      search: "Buscar",
      results: "Resultados",
      noResult: "Nenhum resultado",
      resultOne: "{n} resultado",
      resultMany: "{n} resultados",
      searchPlaceholderId: "Buscar títulos, IDs (por exemplo {example}) e termos",
      searchPlaceholder: "Buscar títulos e termos",
      searchHint: "Enter abre o resultado selecionado · setas movem · Esc fecha",
      nodeLink: "{text}. Pressione Enter para ir à definição.",
      figure: "Figura ",
      figureShort: "Figura",
      figures: "Figuras",
      figureViewer: "Visualizador de figura",
      textSmall: "Texto pequeno: amplie para ler",
      expand: "⤢ Ampliar",
      openFull: "Abrir {title} em tela cheia com zoom",
      viewerHint: "a roda ou o gesto de pinça dão zoom, arrastar move, clique duplo ajusta",
      zoomIn: "Aumentar",
      zoomOut: "Diminuir",
      fit: "Ajustar",
      closeViewer: "Fechar (Esc)"
    }
  };
  /* Captions: the paragraph before a diagram may start with **Figure: Title.** or **Figura: Title.** */
  var CAPTION_PREFIX = /^(?:Figure|Figura):\s*/i;
  var ALL_FEATURES = ["progress", "menu", "spy", "filter", "drawer", "permalinks", "codecopy", "tables",
    "autolink", "abbr", "popover", "back", "search", "slash", "tabs", "figures", "copyopen"];
  var TRIGGERS = "a.ref[data-tip], a.term[data-tip], a.src[data-tip], abbr[data-tip]";

  var doc = document;
  var main = doc.querySelector("main");
  if (!main) return;
  var root = main.closest(".reader-root") || doc.body;
  var nav = doc.querySelector("nav.index");

  /* ---------- UI language: lang starting with "pt" picks pt, anything else en; data-reader-strings overrides ---------- */
  var S = (function () {
    var holder = root.closest("[lang]") || (doc.documentElement.hasAttribute("lang") ? doc.documentElement : null);
    var lang = ((holder && holder.getAttribute("lang")) || "").toLowerCase();
    var pick = lang.indexOf("pt") === 0 ? "pt" : "en", out = {}, k;
    for (k in STRINGS[pick]) out[k] = STRINGS[pick][k];
    var raw = root.getAttribute("data-reader-strings");
    if (raw) {
      try {
        var over = JSON.parse(raw);
        for (k in over) if (Object.prototype.hasOwnProperty.call(over, k) && typeof over[k] === "string") out[k] = over[k];
      } catch (e) { if (window.console) console.warn("Reader: data-reader-strings is not valid JSON"); }
    }
    return out;
  })();
  function say(key, vars) {
    var t = S[key] != null ? S[key] : "";
    if (vars) for (var k in vars) t = t.split("{" + k + "}").join(String(vars[k]));
    return t;
  }
  function plural(n, one, many) { return say(n === 1 ? one : many, { n: n }); }

  /* ---------- Feature switches: data-reader="all -slash" or a list of names ---------- */
  var enabled = (function () {
    var tokens = (main.getAttribute("data-reader") || "").split(/[\s,]+/).filter(Boolean);
    var positive = tokens.filter(function (t) { return t !== "all" && t.charAt(0) !== "-"; });
    var useAll = !tokens.length || tokens.indexOf("all") >= 0 || !positive.length;
    var on = {};
    ALL_FEATURES.forEach(function (f) { on[f] = useAll; });
    positive.forEach(function (f) { on[f] = true; });
    tokens.forEach(function (t) { if (t.charAt(0) === "-") on[t.slice(1)] = false; });
    return on;
  })();
  function has(f) { return !!enabled[f]; }

  /* ---------- Small helpers ---------- */
  function el(tag, cls, text) {
    var e = doc.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function qsa(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }
  function byId(id) { return id ? doc.getElementById(id) : null; }
  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  function tokenOf(href) {
    if (!href || href.charAt(0) !== "#" || href.length < 2) return "";
    try { return decodeURIComponent(href.slice(1)); } catch (e) { return href.slice(1); }
  }
  function setHash(id) {
    if (!/^[A-Za-z0-9_-]+$/.test(id)) return;
    try { history.replaceState(null, "", "#" + id); } catch (e) { /* sandboxed frame */ }
  }
  function slug(s) {
    return String(s).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "section";
  }
  function visible(n) { return !!(n && n.getClientRects().length); }
  function headingText(h) {
    var out = "";
    Array.prototype.forEach.call(h.childNodes, function (c) {
      if (c.nodeType === 1 && c.classList.contains("hlink")) return;
      out += c.textContent;
    });
    return out.replace(/\s+/g, " ").trim();
  }
  function whereOf(node) {
    var d = node.closest && node.closest("[data-doc]");
    if (d) return d.getAttribute("data-doc");
    var p = node.closest && node.closest('[role="tabpanel"]');
    return p ? (p.getAttribute("data-tab-label") || "") : "";
  }
  function short(text, max) {
    var t = String(text).replace(/\s+/g, " ").trim();
    if (t.length <= max) return t;
    var m = t.match(/^(.+?[.!?])(\s|$)/);
    if (m && m[1].length <= max) return m[1];
    return t.slice(0, max - 1).replace(/\s+\S*$/, "") + "…";
  }

  /* Live region: announces Copied, Returned, result counts. */
  var liveEl = el("div", "sr-only"); liveEl.setAttribute("role", "status"); liveEl.setAttribute("aria-live", "polite");
  root.appendChild(liveEl);
  var liveTimer = null;
  function live(msg) {
    liveEl.textContent = msg;
    clearTimeout(liveTimer);
    liveTimer = setTimeout(function () { liveEl.textContent = ""; }, T.LIVE_CLEAR_MS);
  }

  /* Copy without window.prompt: Clipboard API, then execCommand, then select the text for Ctrl+C. */
  function legacyCopy(text) {
    var ta = el("textarea"); ta.value = text; ta.setAttribute("readonly", ""); ta.className = "sr-only";
    root.appendChild(ta); ta.select();
    var ok = false;
    try { ok = doc.execCommand("copy"); } catch (e) { ok = false; }
    root.removeChild(ta);
    return ok;
  }
  function selectFallback(text, btn, selectEl) {
    if (selectEl) {
      var r = doc.createRange(); r.selectNodeContents(selectEl);
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      return;
    }
    var inp = el("input", "copyfallback"); inp.type = "text"; inp.readOnly = true; inp.value = text;
    inp.setAttribute("aria-label", say("textToCopy"));
    btn.parentNode.insertBefore(inp, btn.nextSibling);
    inp.focus(); inp.select();
    var drop = function () { if (inp.parentNode) inp.parentNode.removeChild(inp); };
    inp.addEventListener("blur", drop);
    inp.addEventListener("keydown", function (ev) { if (ev.key === "Escape" || ev.key === "Enter") { drop(); btn.focus(); } });
  }
  function copyText(text, btn, label, selectEl) {
    var restore = function () { setTimeout(function () { btn.textContent = label; }, T.COPIED_MS); };
    var ok = function () { btn.textContent = say("copied"); live(say("copiedLive")); restore(); };
    var fail = function () {
      selectFallback(text, btn, selectEl);
      btn.textContent = say("selectedCopy"); live(say("selectedLive")); restore();
    };
    var legacy = function () { var done = false; try { done = legacyCopy(text); } catch (e) { done = false; } if (done) ok(); else fail(); };
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(ok, legacy); return; }
    } catch (e) { /* fall through */ }
    legacy();
  }

  /* ---------- Heading ids: every h2 to h4 gets a stable slug when it has none ---------- */
  (function ensureHeadingIds() {
    var used = {};
    qsa("[id]", doc).forEach(function (n) { used[n.id] = 1; });
    qsa("h2, h3, h4", main).forEach(function (h) {
      if (h.id || h.hasAttribute("data-noid")) return;
      var base = slug(headingText(h)), id = base, n = 2;
      while (used[id]) id = base + "-" + (n++);
      used[id] = 1; h.id = id;
    });
  })();

  /* ---------- ID grammar from data-id-prefixes: R,Q,ADR- -> R12, Q13b, ADR-4 ---------- */
  var prefixes = (main.getAttribute("data-id-prefixes") || "").split(/[\s,]+/).filter(Boolean)
    .sort(function (a, b) { return b.length - a.length; });
  var idCore = prefixes.length ? "(?:" + prefixes.map(esc).join("|") + ")\\d+[a-z]?" : "";
  var idFull = idCore ? new RegExp("^" + idCore + "$") : null;
  var idFind = idCore ? new RegExp("(^|[^\\w-])(" + idCore + ")(?![\\w-])") : null;
  function isId(s) { return !!(idFull && idFull.test(s)); }

  /* ---------- Tabs: one tabpanel per type; any link, hit or hash into a hidden tab opens it ---------- */
  var tabBar = main.querySelector('.tabs[role="tablist"]');
  var tabs = tabBar ? qsa('[role="tab"]', tabBar) : [];
  var panels = [];
  tabs.forEach(function (t) {
    var p = byId(t.getAttribute("aria-controls"));
    if (p) { panels.push(p); p.setAttribute("data-tab-label", t.textContent.trim()); }
  });
  function tabOf(panel) { return byId(panel.getAttribute("aria-labelledby")); }
  function activeTab() { return tabs.filter(function (t) { return t.getAttribute("aria-selected") === "true"; })[0] || null; }
  function tabsHeight() { return tabBar ? tabBar.getBoundingClientRect().height : 0; }
  function setTabsVar() { if (tabBar) root.style.setProperty("--tabs-h", Math.round(tabsHeight()) + "px"); }
  var onTabChange = [];
  function activate(tab, user) {
    if (!tab) return;
    tabs.forEach(function (t) {
      var on = t === tab, p = byId(t.getAttribute("aria-controls"));
      t.setAttribute("aria-selected", on ? "true" : "false"); t.tabIndex = on ? 0 : -1;
      if (p) p.hidden = !on;
    });
    /* Scroll only the tab bar sideways: scrollIntoView would also move the page, and on load that hides In one minute. */
    if (tabBar) {
      var bar = tabBar.getBoundingClientRect(), tb = tab.getBoundingClientRect();
      if (tb.left < bar.left) tabBar.scrollLeft -= bar.left - tb.left;
      else if (tb.right > bar.right) tabBar.scrollLeft += tb.right - bar.right;
    }
    onTabChange.forEach(function (fn) { fn(); });
    if (user) {
      var p = byId(tab.getAttribute("aria-controls"));
      if (p) {
        setHash(p.id);
        var top = p.getBoundingClientRect().top + window.scrollY - tabsHeight() - T.POP_EDGE_PX;
        if (window.scrollY > top) window.scrollTo(0, Math.max(0, top));
      }
    }
  }
  /* reveal(id): opens the tab that holds the target and returns the target */
  function reveal(id) {
    var target = byId(id);
    if (!target) return null;
    if (has("tabs")) {
      var panel = target.closest('[role="tabpanel"]');
      if (panel && panel.hidden) activate(tabOf(panel), false);
    }
    return target;
  }
  function inHiddenPanel(n) { var p = n.closest && n.closest('[role="tabpanel"]'); return !!(p && p.hidden); }
  if (has("tabs") && tabs.length) {
    var startHash = tokenOf(location.hash), startPanel = startHash && byId(startHash) && byId(startHash).closest('[role="tabpanel"]');
    var first = (startPanel && tabOf(startPanel)) || activeTab() || tabs[0];
    activate(first, false);
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { activate(t, true); });
      t.addEventListener("keydown", function (ev) {
        var k = ev.key, n = null;
        if (k === "ArrowRight") n = tabs[(i + 1) % tabs.length];
        else if (k === "ArrowLeft") n = tabs[(i + tabs.length - 1) % tabs.length];
        else if (k === "Home") n = tabs[0];
        else if (k === "End") n = tabs[tabs.length - 1];
        if (n) { activate(n, true); n.focus(); ev.preventDefault(); }
      });
    });
    setTabsVar();
    window.addEventListener("resize", setTabsVar);
  }

  /* ---------- Target mark: replaceState does not update :target, so jumps add .is-target ---------- */
  var marked = null;
  function markTarget(t) {
    if (marked) marked.classList.remove("is-target");
    marked = null;
    if (!t || t.getAttribute("role") === "tabpanel" || t === main) return;
    t.classList.add("is-target"); marked = t;
  }

  /* ---------- Back to where you were ---------- */
  var backBtn = null, ret = null;
  if (has("back")) {
    backBtn = el("button", null, say("back")); backBtn.id = "back"; backBtn.type = "button";
    root.appendChild(backBtn);
    backBtn.addEventListener("click", function () {
      if (ret) {
        if (ret.tab && has("tabs")) activate(ret.tab, false);
        window.scrollTo(0, ret.y);
        live(say("returned"));
      }
      ret = null; backBtn.classList.remove("show"); hidePop();
    });
  }
  function armBack() {
    if (!backBtn) return;
    ret = { y: window.scrollY, tab: activeTab() }; backBtn.classList.add("show");
  }

  /* jump(id): reveal the tab, scroll, mark, set a plain hash, move focus; used by search, nodes, menu */
  function jump(id, opts) {
    var target = reveal(id);
    if (!target) return;
    if (!(opts && opts.noBack)) armBack();
    target.scrollIntoView({ block: "start" });
    markTarget(target); setHash(id);
    if (!target.hasAttribute("tabindex")) target.setAttribute("tabindex", "-1");
    try { target.focus({ preventScroll: true }); } catch (e) { /* old engine */ }
  }

  /* ---------- Auto-linking fallback: glossary terms and defined IDs, first mention per block ---------- */
  var autolinked = false;
  function initAutolink() {
    var BLOCK = "p, li, td, th, dd, dt, blockquote, figcaption, summary";
    var SKIP = "a, code, pre, h1, h2, h3, h4, h5, h6, abbr, button, script, style, textarea, select, nav, svg, " +
      ".defid, .defterm, .tag, .hlink, .copy, .pop, .mermaid, .diagram, .figbar, [data-no-link]";
    // Plain glossary tables (data-glossary): wrap the first cell so it becomes a definition target.
    // A column headed Aliases (case-insensitive, comma-separated) becomes data-aliases on the term.
    qsa("table[data-glossary]", main).forEach(function (tbl) {
      var aliasCol = -1, head = tbl.querySelector("tr");
      if (head && head.querySelector("th")) {
        qsa("th, td", head).forEach(function (c, i) { if (c.textContent.trim().toLowerCase() === "aliases") aliasCol = i; });
      }
      qsa("tr", tbl).forEach(function (tr) {
        var cell = tr.querySelector("td");
        if (!cell || cell.querySelector(".defterm")) return;
        var name = cell.textContent.trim(); if (!name) return;
        var s = el("span", "defterm"); s.id = "term-" + slug(name);
        var cells = qsa("th, td", tr);
        if (aliasCol > 0 && cells[aliasCol]) { var al = cells[aliasCol].textContent.trim(); if (al) s.setAttribute("data-aliases", al); }
        while (cell.firstChild) s.appendChild(cell.firstChild);
        cell.appendChild(s);
      });
    });
    var defs = {}, termMap = {}, owner = {};
    function defTextFor(node, name) {
      var row = node.closest("tr"), txt = "";
      if (node.tagName === "DT") { var dd = node.nextElementSibling; while (dd && dd.tagName !== "DD") dd = dd.nextElementSibling; txt = dd ? dd.textContent : ""; owner[node.id] = dd; }
      else if (row) { var cells = qsa("td, th", row), i = cells.indexOf(node.closest("td, th")); txt = cells[i + 1] ? cells[i + 1].textContent : row.textContent; owner[node.id] = row; }
      else { var li = node.closest("li, p") || node.parentElement; txt = li ? li.textContent.replace(name, "") : ""; owner[node.id] = li; }
      return txt.replace(/^[\s.:–—-]+/, "");
    }
    qsa(".defterm[id^='term-']", main).forEach(function (n) {
      var name = n.textContent.replace(/\s+/g, " ").trim(); if (!name) return;
      var names = [name].concat((n.getAttribute("data-aliases") || "").split(",").map(function (s) { return s.trim(); }).filter(Boolean));
      var tip = name + T.POP_TIP_SEP + short(defTextFor(n, name), T.SHORT_TIP_MAX);
      names.forEach(function (nm) { if (!termMap[nm]) termMap[nm] = { kind: "term", id: n.id, tip: tip }; });
    });
    qsa(".defid[id^='def-']", main).forEach(function (n) {
      var id = n.id.slice(4);
      var body = defTextFor(n, n.textContent.trim());
      defs[id] = { kind: "ref", id: n.id, tip: id + T.POP_TIP_SEP + short(body, T.SHORT_TIP_MAX) };
    });
    var names = Object.keys(termMap).sort(function (a, b) { return b.length - a.length; });
    if (!names.length && !Object.keys(defs).length && !idCore) return;
    var alts = [];
    if (idCore) alts.push(idCore);
    names.forEach(function (n) { alts.push(esc(n) + "(?:s|es)?"); });
    var rx = new RegExp("(^|[^\\w-])(" + alts.join("|") + ")(?![\\w-])", "g");
    function resolve(word) {
      if (isId(word)) return defs[word] || { kind: "ref", missing: true, label: word };
      return termMap[word] || termMap[word.replace(/s$/, "")] || termMap[word.replace(/es$/, "")] || null;
    }
    // Existing links count as the first mention in their block.
    var seenByBlock = new Map();
    function seenFor(block) { var s = seenByBlock.get(block); if (!s) { s = {}; seenByBlock.set(block, s); } return s; }
    qsa("a.term[href^='#term-'], a.ref[href^='#def-']", main).forEach(function (a) { var b = a.closest(BLOCK); if (b) seenFor(b)[tokenOf(a.getAttribute("href"))] = 1; });
    var walker = doc.createTreeWalker(main, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        var p = n.parentElement;
        return p && !p.closest(SKIP) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    var nodes = [], n;
    while ((n = walker.nextNode())) nodes.push(n);
    var missing = {};
    nodes.forEach(function (node) {
      var text = node.nodeValue, last = 0, m, frag = null;
      var block = node.parentElement.closest(BLOCK) || node.parentElement;
      rx.lastIndex = 0;
      while ((m = rx.exec(text))) {
        var lead = m[1], word = m[2], hit = resolve(word);
        if (!hit) { rx.lastIndex = m.index + m[0].length; continue; }
        var start = m.index + lead.length;
        if (hit.id && owner[hit.id] === block) continue;              // a definition does not link to itself
        if (hit.id) { var s = seenFor(block); if (s[hit.id]) continue; s[hit.id] = 1; }  // first mention per block, terms and IDs alike
        if (!frag) frag = doc.createDocumentFragment();
        frag.appendChild(doc.createTextNode(text.slice(last, start)));
        var a;
        if (hit.missing) { a = el("span", "ref missing", word); a.title = say("noDefinition"); missing[word] = 1; }
        else {
          a = el("a", hit.kind === "term" ? "term" : "ref", word); a.href = "#" + hit.id;
          a.setAttribute("data-tip", hit.tip); a.setAttribute("data-auto", "1");
        }
        frag.appendChild(a); last = start + word.length;
      }
      if (frag) { frag.appendChild(doc.createTextNode(text.slice(last))); node.parentNode.replaceChild(frag, node); }
    });
    var list = Object.keys(missing);
    if (list.length && window.console) console.warn("Reader: IDs used but not defined: " + list.sort().join(", "));
    autolinked = true;
  }
  if (has("autolink")) initAutolink();

  /* ---------- Abbreviations: abbr[title] becomes keyboard and touch friendly through the popover ---------- */
  if (has("abbr") && has("popover")) {
    qsa("abbr[title]", main).forEach(function (a) {
      var exp = a.getAttribute("title"); if (!exp) return;
      a.setAttribute("data-tip", a.textContent.trim() + T.POP_TIP_SEP + exp);
      a.removeAttribute("title"); a.tabIndex = 0;
    });
  }

  /* ---------- Where each defined ID or term is used: one pass, nearest heading before it ---------- */
  var uses = {}, secOf = new Map();
  (function indexUses() {
    var cur = null, n = 0;
    qsa("h2, h3, h4, a.ref[data-tip], a.term[data-tip]", main).forEach(function (n2) {
      if (/^H\d$/.test(n2.tagName)) { cur = n2; return; }
      var href = n2.getAttribute("href") || "";
      if (!/^#(def|term)-/.test(href)) return;
      if (!n2.id) n2.id = "use-" + (n++);
      secOf.set(n2, { id: cur ? cur.id : "", text: cur ? headingText(cur) : "", doc: whereOf(n2) });
      (uses[href] = uses[href] || []).push(n2);
    });
  })();

  /* ---------- Contents menu: build when empty, search button, filter, figure index, drawer ---------- */
  function buildMenu() {
    var ul = el("ul"), groups = {}, order = [];
    function groupOf(h) {
      var p = h.closest('[role="tabpanel"]'), key = p ? p.id : "";
      if (!groups[key]) { groups[key] = { panel: p, items: [] }; order.push(key); }
      return groups[key];
    }
    qsa("h2[id], h3[id]", main).forEach(function (h) {
      if (h.hasAttribute("data-nomenu") || h.closest("nav, .pop")) return;
      groupOf(h).items.push(h);
    });
    order.forEach(function (key) {
      var g = groups[key], holder = ul;
      if (g.panel) {
        var li0 = el("li"), a0 = el("a", "navdoc", g.panel.getAttribute("data-tab-label") || g.panel.id);
        a0.href = "#" + g.panel.id; li0.appendChild(a0);
        holder = el("ul"); li0.appendChild(holder); ul.appendChild(li0);
      }
      var lastH2 = null, sub = null;
      g.items.forEach(function (h) {
        var li = el("li"), a = el("a", !g.panel && h.tagName === "H2" ? "navdoc" : null, headingText(h));
        a.href = "#" + h.id; li.appendChild(a);
        if (h.tagName === "H2" || !lastH2) {
          holder.appendChild(li);
          if (h.tagName === "H2") { lastH2 = li; sub = null; }
        } else {
          if (!sub) { sub = el("ul"); lastH2.appendChild(sub); }
          sub.appendChild(li);
        }
      });
    });
    nav.appendChild(ul);
  }
  var menuList = null, figList = null;
  if (nav && has("menu")) {
    if (!nav.querySelector("ul")) buildMenu();
    menuList = nav.querySelector("ul");
    if (!nav.id) nav.id = "contents";
  }

  var searchBtn = doc.getElementById("searchbtn");
  if (nav && has("search") && !searchBtn) {
    searchBtn = el("button", "searchbtn", has("slash") ? say("searchBtnSlash") : say("searchBtn"));
    searchBtn.id = "searchbtn"; searchBtn.type = "button"; nav.insertBefore(searchBtn, nav.firstChild);
  }

  /* Filter box: matches a link or any link below it; a matching parent keeps all its children */
  if (nav && menuList && has("filter")) {
    var filterWrap = el("div", "navfilterwrap");
    var f = el("input", "navfilter"); f.type = "search"; f.placeholder = say("filter"); f.setAttribute("aria-label", say("filter"));
    filterWrap.appendChild(f);
    nav.insertBefore(filterWrap, menuList);
    var noMatch = el("p", "navempty", say("noMatch")); noMatch.hidden = true; nav.insertBefore(noMatch, menuList);
    var filterTimer = null;
    var applyFilter = function () {
      var q = f.value.trim().toLowerCase(), hits = 0;
      var walk = function (li, parentHit) {
        var a = null, kids = [];
        Array.prototype.forEach.call(li.children, function (c) {
          if (c.tagName === "A" && !a) a = c;
          if (c.tagName === "UL") kids = kids.concat(Array.prototype.slice.call(c.children));
        });
        var own = !!(a && a.textContent.toLowerCase().indexOf(q) >= 0), any = false;
        if (own && q) hits++;
        kids.forEach(function (k) { if (walk(k, parentHit || own)) any = true; });
        var show = !q || own || parentHit || any;
        li.hidden = !show;
        return show;
      };
      Array.prototype.forEach.call(menuList.children, function (li) { walk(li, false); });
      noMatch.hidden = !q || hits > 0;
      if (q) live(plural(hits, "matchOne", "matchMany"));
    };
    f.addEventListener("input", function () { clearTimeout(filterTimer); filterTimer = setTimeout(applyFilter, T.FILTER_DEBOUNCE_MS); });
    f.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && f.value) { f.value = ""; applyFilter(); ev.stopPropagation(); }
    });
  }

  /* Drawer for phones: the same <nav> opens as a panel from a Contents button */
  var navOpen = false, menuBtn = null, scrim = null, drawerReturn = null;
  if (nav && has("drawer")) {
    menuBtn = el("button", "menubtn", say("menuBtn")); menuBtn.type = "button"; menuBtn.id = "menubtn";
    menuBtn.setAttribute("aria-controls", nav.id || "contents"); menuBtn.setAttribute("aria-expanded", "false");
    if (!nav.id) nav.id = "contents";
    scrim = el("div", "navscrim"); scrim.hidden = true;
    root.appendChild(menuBtn); root.appendChild(scrim);
    var closeBtn = el("button", "navclose", say("closeMenu")); closeBtn.type = "button";
    nav.insertBefore(closeBtn, nav.firstChild);
    var setDrawer = function (open) {
      navOpen = open;
      root.classList.toggle("nav-open", open);
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      scrim.hidden = !open;
      if (open) {
        drawerReturn = doc.activeElement;
        var firstFocus = nav.querySelector("button, input, a"); if (firstFocus) firstFocus.focus();
      } else if (drawerReturn && drawerReturn.focus) { drawerReturn.focus(); drawerReturn = null; }
    };
    menuBtn.addEventListener("click", function () { setDrawer(!navOpen); });
    closeBtn.addEventListener("click", function () { setDrawer(false); });
    scrim.addEventListener("click", function () { setDrawer(false); });
    nav.addEventListener("click", function (ev) { if (navOpen && ev.target.closest && ev.target.closest("a[href^='#']")) { navOpen = false; root.classList.remove("nav-open"); menuBtn.setAttribute("aria-expanded", "false"); scrim.hidden = true; drawerReturn = null; } });
    nav.addEventListener("keydown", function (ev) {
      if (!navOpen || ev.key !== "Tab") return;
      var items = qsa("button, input, a[href]", nav).filter(visible);
      if (!items.length) return;
      var firstEl = items[0], lastEl = items[items.length - 1];
      if (ev.shiftKey && doc.activeElement === firstEl) { lastEl.focus(); ev.preventDefault(); }
      else if (!ev.shiftKey && doc.activeElement === lastEl) { firstEl.focus(); ev.preventDefault(); }
    });
    window.addEventListener("resize", function () { if (navOpen && window.innerWidth > T.DRAWER_BREAKPOINT_PX) setDrawer(false); });
    doc.addEventListener("keydown", function (ev) { if (ev.key === "Escape" && navOpen) setDrawer(false); });
  }
  function closeDrawer() { if (navOpen && menuBtn) menuBtn.click(); }

  /* ---------- Heading permalinks (h2 to h4) ---------- */
  if (has("permalinks")) {
    qsa("h2[id], h3[id], h4[id]", main).forEach(function (h) {
      if (h.querySelector(".hlink")) return;
      var b = el("button", "hlink", "#"); b.type = "button";
      b.setAttribute("aria-label", say("copyLinkTo", { name: headingText(h) }));
      b.addEventListener("click", function (ev) {
        ev.stopPropagation();
        copyText(location.href.split("#")[0] + "#" + h.id, b, "#");
      });
      h.appendChild(b);
    });
  }

  /* ---------- Code copy ---------- */
  if (has("codecopy")) {
    qsa("pre:not(.mermaid)", main).forEach(function (pre) {
      if (pre.closest(".codewrap, .diagram")) return;
      var wrap = el("div", "codewrap"); pre.parentNode.insertBefore(wrap, pre); wrap.appendChild(pre);
      var b = el("button", "codecopy", say("copy")); b.type = "button";
      b.setAttribute("aria-label", say("copyCode"));
      b.addEventListener("click", function () { copyText(pre.innerText.replace(/\n$/, ""), b, say("copy"), pre); });
      wrap.appendChild(b);
    });
  }

  /* ---------- Tables: wrap, and make a scrolling wrapper reachable with the keyboard ---------- */
  var tableWraps = [];
  function markScrollable() {
    tableWraps.forEach(function (w) {
      var scrolls = w.scrollWidth > w.clientWidth + 1;
      if (scrolls) { w.tabIndex = 0; w.setAttribute("role", "region"); if (!w.hasAttribute("aria-label")) w.setAttribute("aria-label", say("scrollTable")); }
      else if (w.getAttribute("aria-label") === say("scrollTable")) { w.removeAttribute("tabindex"); w.removeAttribute("role"); w.removeAttribute("aria-label"); }
    });
  }
  if (has("tables")) {
    qsa("table", main).forEach(function (t) {
      if (t.closest(".tablewrap")) return;
      var w = el("div", "tablewrap"); t.parentNode.insertBefore(w, t); w.appendChild(t);
    });
    tableWraps = qsa(".tablewrap", main);
    markScrollable();
    window.addEventListener("resize", markScrollable);
    onTabChange.push(markScrollable);
  }

  /* ---------- Open questions: copy keeps the IDs ---------- */
  if (has("copyopen")) {
    qsa("button.copy[data-target]", main).forEach(function (btn) {
      btn.addEventListener("click", function () {
        var list = byId(btn.getAttribute("data-target"));
        if (!list) return;
        var text = Array.prototype.map.call(list.children, function (li, i) {
          var q = li.querySelector(".q"), a = li.querySelector(".a"), tag = li.querySelector(".tag");
          return (i + 1) + ". " + (tag ? "[" + tag.textContent.trim() + "] " : "") + (q ? q.textContent.trim() : li.textContent.trim()) + (a ? " " + a.textContent.trim() : "");
        }).join("\n");
        copyText(text, btn, btn.getAttribute("data-label") || btn.textContent || say("copy"), list);
      });
    });
  }

  /* ---------- Popover: hover, focus, tap; hoverable and persistent; Esc; reachable with Tab ---------- */
  var pop = null, openFor = null, closeTimer = null, lastPointer = "mouse", skipFocusOpen = false;
  function hidePop() {
    if (!pop || pop.hidden) { openFor = null; return; }
    pop.hidden = true;
    if (openFor) openFor.removeAttribute("aria-describedby");
    openFor = null;
  }
  function laterHide() { clearTimeout(closeTimer); closeTimer = setTimeout(hidePop, T.POP_CLOSE_DELAY_MS); }
  function triggerOf(ev) { return ev.target.closest && ev.target.closest(TRIGGERS); }
  function placePop(a) {
    var r = a.getBoundingClientRect();
    var top = window.scrollY + r.bottom + T.POP_GAP_PX, left = window.scrollX + r.left;
    pop.style.top = top + "px"; pop.style.left = "0px";
    var w = pop.offsetWidth, maxLeft = window.scrollX + doc.documentElement.clientWidth - w - T.POP_EDGE_PX;
    pop.style.left = Math.max(T.POP_EDGE_PX, Math.min(left, maxLeft)) + "px";
    if (r.bottom + pop.offsetHeight + 2 * T.POP_GAP_PX > window.innerHeight && r.top > pop.offsetHeight + 2 * T.POP_GAP_PX) {
      pop.style.top = (window.scrollY + r.top - pop.offsetHeight - T.POP_GAP_PX) + "px";
    }
  }
  function usesLine(href, a) {
    var list = uses[href] || [];
    var line = el("div", "pu");
    line.appendChild(doc.createTextNode(plural(list.length, "usedOne", "usedMany") + (list.length ? ": " : "")));
    var groups = [], byKey = {};
    list.forEach(function (u) {
      var s = secOf.get(u) || { id: "", text: "", doc: "" }, key = s.doc + "|" + s.id;
      var g = byKey[key];
      if (!g) { g = byKey[key] = { sec: s, anchor: null, count: 0 }; groups.push(g); }
      if (u === a) return;
      g.count++; if (!g.anchor) g.anchor = u;
    });
    groups = groups.filter(function (g) { return g.count > 0; });
    var addItem = function (g, idx) {
      var label = (g.sec.doc ? g.sec.doc + (g.sec.text ? " › " : "") : "") + g.sec.text;
      var l = el("a", null, (label || say("thisPage")) + (g.count > 1 ? " (×" + g.count + ")" : "")); l.href = "#" + g.anchor.id;
      if (idx > 0) line.appendChild(doc.createTextNode(" · "));
      line.appendChild(l);
    };
    groups.slice(0, T.POP_MAX_USES).forEach(addItem);
    if (groups.length > T.POP_MAX_USES) {
      var more = el("button", "pmore", say("more", { n: groups.length - T.POP_MAX_USES })); more.type = "button";
      more.addEventListener("click", function (ev) {
        ev.stopPropagation();
        line.removeChild(more);
        groups.slice(T.POP_MAX_USES).forEach(function (g, i) { addItem(g, T.POP_MAX_USES + i); });
        if (openFor) placePop(openFor);
      });
      line.appendChild(doc.createTextNode(" · ")); line.appendChild(more);
    }
    return line;
  }
  function showPop(a) {
    clearTimeout(closeTimer);
    if (openFor === a) return;
    if (openFor) openFor.removeAttribute("aria-describedby");
    var tip = a.getAttribute("data-tip") || "", cut = tip.indexOf(T.POP_TIP_SEP);
    pop.textContent = "";
    pop.appendChild(el("div", "ph", cut > 0 ? tip.slice(0, cut) : tip));
    if (cut > 0) pop.appendChild(el("div", "pb", tip.slice(cut + T.POP_TIP_SEP.length)));
    var href = a.getAttribute("href") || a.getAttribute("data-href") || "";
    if (/^#(def|term)-/.test(href)) pop.appendChild(usesLine(href, a));
    if (href) {
      var pa = el("div", "pa"), external = !!(a.classList && a.classList.contains("src"));
      var go = el("a", null, external ? (a.getAttribute("data-action") || say("openSource")) : say("goDefinition"));
      go.href = href; if (external) { go.target = "_blank"; go.rel = "noopener"; }
      pa.appendChild(go); pop.appendChild(pa);
    }
    pop.hidden = false; placePop(a);
    openFor = a; a.setAttribute("aria-describedby", "pop");
  }
  if (has("popover")) {
    pop = el("div", "pop"); pop.id = "pop"; pop.setAttribute("role", "tooltip"); pop.hidden = true;
    root.appendChild(pop);
    doc.addEventListener("pointerdown", function (ev) { lastPointer = ev.pointerType || "mouse"; }, true);
    main.addEventListener("pointerover", function (ev) { if (ev.pointerType === "touch") return; var a = triggerOf(ev); if (a) showPop(a); });
    main.addEventListener("pointerout", function (ev) { if (ev.pointerType === "touch") return; if (triggerOf(ev)) laterHide(); });
    main.addEventListener("focusin", function (ev) {
      var a = triggerOf(ev);
      if (!a) return;
      if (skipFocusOpen) { skipFocusOpen = false; return; }
      showPop(a);
    });
    main.addEventListener("focusout", function (ev) { if (!pop.contains(ev.relatedTarget)) laterHide(); });
    pop.addEventListener("mouseenter", function () { clearTimeout(closeTimer); });
    pop.addEventListener("mouseleave", laterHide);
    pop.addEventListener("focusin", function () { clearTimeout(closeTimer); });
    pop.addEventListener("focusout", function (ev) { if (!pop.contains(ev.relatedTarget) && ev.relatedTarget !== openFor) laterHide(); });
    pop.addEventListener("click", function (ev) { if (ev.target.closest && ev.target.closest("a")) hidePop(); });
    // Keyboard: Tab from an open trigger enters the popover links; Tab out of it returns to the trigger.
    main.addEventListener("keydown", function (ev) {
      var a = triggerOf(ev);
      if (ev.key !== "Tab" || ev.shiftKey || !a || openFor !== a || pop.hidden) return;
      var firstLink = pop.querySelector("a, button");
      if (firstLink) { ev.preventDefault(); firstLink.focus(); }
    });
    pop.addEventListener("keydown", function (ev) {
      if (ev.key !== "Tab" && ev.key !== "Escape") return;
      var items = qsa("a, button", pop), idx = items.indexOf(doc.activeElement);
      var leaving = ev.key === "Escape" || (ev.shiftKey && idx <= 0) || (!ev.shiftKey && idx === items.length - 1);
      if (!leaving) return;
      var back = openFor;
      ev.preventDefault(); hidePop();
      if (back && back.focus) { skipFocusOpen = true; back.focus(); }
    });
    // Touch: the first tap on a trigger opens the popover; the second follows the link.
    main.addEventListener("click", function (ev) {
      var a = triggerOf(ev);
      if (a && lastPointer === "touch" && openFor !== a && a.tagName === "A") { ev.preventDefault(); showPop(a); }
      else if (a && a.tagName === "ABBR" && lastPointer === "touch") showPop(a);
    });
    doc.addEventListener("click", function (ev) {
      if (!pop.hidden && !pop.contains(ev.target) && !(openFor && openFor.contains(ev.target))) hidePop();
    });
    window.addEventListener("resize", hidePop);
  }

  /* ---------- One handler for in-page links: reveal hidden tabs, arm the back pill ---------- */
  doc.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a[href^='#']");
    if (!a || ev.button || ev.metaKey || ev.ctrlKey || ev.shiftKey || ev.altKey) return;
    var id = tokenOf(a.getAttribute("href"));
    if (!id || a.classList.contains("skip")) return;
    if (pop && a.matches("a.ref, a.term") && lastPointer === "touch" && openFor !== a) return;   // first tap only opens
    var target = byId(id);
    if (!target) return;
    var fromMenu = !!a.closest("nav.index, #search");
    if (!fromMenu) armBack();                                    // menu and search jumps never arm the pill
    if (inHiddenPanel(target)) {
      ev.preventDefault(); reveal(id);
      target.scrollIntoView({ block: "start" }); markTarget(target); setHash(id);
    } else { setTimeout(function () { markTarget(target); }, 0); }
  }, true);
  window.addEventListener("hashchange", function () {
    var t = reveal(tokenOf(location.hash));
    if (t) { t.scrollIntoView({ block: "start" }); markTarget(t); }
  });

  /* ---------- Reading progress, scroll spy, back-pill hide: one scroll handler ---------- */
  var progressBar = null;
  if (has("progress")) {
    progressBar = el("div"); progressBar.id = "progress"; progressBar.setAttribute("aria-hidden", "true");
    root.appendChild(progressBar);
  }
  var spyLinks = {}, spyHeads = [], spyCurrent = null;
  if (nav && has("spy") && menuList) {
    qsa("a[href^='#']", nav).forEach(function (a) { var id = tokenOf(a.getAttribute("href")); if (id && !spyLinks[id]) spyLinks[id] = a; });
    spyHeads = Object.keys(spyLinks).map(byId).filter(Boolean).sort(function (a, b) {
      return a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
    });
  }
  function navScrollTo(a) {
    if (!visible(nav)) return;
    var r = a.getBoundingClientRect(), nr = nav.getBoundingClientRect();
    if (r.top < nr.top || r.bottom > nr.bottom) nav.scrollTop += r.top - nr.top - nr.height * T.NAV_SCROLL_RATIO;
  }
  function spy() {
    var line = window.innerHeight * T.SPY_LINE_RATIO, best = null;
    for (var i = 0; i < spyHeads.length; i++) {
      var h = spyHeads[i];
      if (!visible(h)) continue;                                  // headings of hidden tabs do not count
      if (h.getBoundingClientRect().top <= line) best = h; else break;
    }
    var a = best ? spyLinks[best.id] : null;
    if (a === spyCurrent) return;
    if (spyCurrent) { spyCurrent.classList.remove("active"); spyCurrent.removeAttribute("aria-current"); }
    spyCurrent = a;
    if (a) { a.classList.add("active"); a.setAttribute("aria-current", "location"); navScrollTo(a); }
  }
  var ticking = false;
  function onScroll() {
    ticking = false;
    if (progressBar) {
      var h = doc.documentElement, max = h.scrollHeight - h.clientHeight;
      progressBar.style.transform = "scaleX(" + (max > 0 ? Math.min(1, Math.max(0, h.scrollTop / max)) : 0) + ")";
    }
    if (spyHeads.length) spy();
    if (ret && backBtn && Math.abs(window.scrollY - ret.y) < T.BACK_NEAR_PX && ret.tab === activeTab()) {
      ret = null; backBtn.classList.remove("show");
    }
  }
  window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener("resize", function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } });
  onTabChange.push(function () { requestAnimationFrame(onScroll); });
  onScroll();

  /* ---------- Search: / or Ctrl+K; all words match; exact ID or term first; headings before definitions ---------- */
  var searchBox = null, searchInput = null, searchList = null, searchIndex = null, searchSel = 0, searchResults = [], searchReturn = null;
  function searchOpen() { return !!(searchBox && searchBox.classList.contains("open")); }
  function buildIndex() {
    searchIndex = [];
    qsa("h2[id], h3[id], h4[id]", main).forEach(function (h) {
      searchIndex.push({ id: h.id, label: headingText(h), where: whereOf(h), kind: 0, key: "" });
    });
    qsa(".diagram[id]", main).forEach(function (d) {
      var no = d.querySelector(".figno");
      if (no) searchIndex.push({ id: d.id, label: no.textContent.trim(), where: whereOf(d), kind: 0, key: "" });
    });
    var seen = {};
    qsa(".defid[id], .defterm[id]", main).forEach(function (d) {
      if (seen[d.id]) return; seen[d.id] = 1;
      var row = d.closest("tr, li, dt") || d.parentElement;
      var txt = (row ? row.textContent : d.textContent).replace(/\s+/g, " ").trim();
      if (row && row.tagName === "DT" && row.nextElementSibling) txt += " " + row.nextElementSibling.textContent.replace(/\s+/g, " ").trim();
      searchIndex.push({ id: d.id, label: txt.slice(0, T.SEARCH_LABEL_MAX), where: whereOf(d), kind: 1, key: d.textContent.trim().toLowerCase() });
    });
  }
  function appendMarked(a, label, words) {
    var lower = label.toLowerCase(), ranges = [];
    words.forEach(function (w) { var i = lower.indexOf(w); if (i >= 0) ranges.push([i, i + w.length]); });
    ranges.sort(function (x, y) { return x[0] - y[0]; });
    var merged = [];
    ranges.forEach(function (r) { var l = merged[merged.length - 1]; if (l && r[0] <= l[1]) l[1] = Math.max(l[1], r[1]); else merged.push(r.slice()); });
    var pos = 0;
    merged.forEach(function (r) {
      if (r[0] > pos) a.appendChild(doc.createTextNode(label.slice(pos, r[0])));
      a.appendChild(el("mark", null, label.slice(r[0], r[1]))); pos = r[1];
    });
    if (pos < label.length) a.appendChild(doc.createTextNode(label.slice(pos)));
  }
  function renderResults(words) {
    searchList.textContent = "";
    var shown = searchResults.slice(0, T.SEARCH_MAX_ROWS);
    shown.forEach(function (r, i) {
      var li = el("li"); li.setAttribute("role", "presentation");
      var a = el("a"); a.href = "#" + r.id; a.id = "sr-" + i;
      a.setAttribute("role", "option"); a.setAttribute("aria-selected", i === searchSel ? "true" : "false");
      appendMarked(a, r.label, words);
      if (r.where) a.appendChild(el("span", "w", r.where));
      a.addEventListener("click", function (ev) { ev.preventDefault(); closeSearch(false); jump(r.id); });
      li.appendChild(a); searchList.appendChild(li);
    });
    if (!shown.length && searchInput.value.trim()) {
      var none = el("li", "none", say("noResult")); none.setAttribute("role", "presentation"); searchList.appendChild(none);
    }
    searchInput.setAttribute("aria-expanded", shown.length ? "true" : "false");
    if (shown.length) searchInput.setAttribute("aria-activedescendant", "sr-" + searchSel); else searchInput.removeAttribute("aria-activedescendant");
    var sel = byId("sr-" + searchSel); if (sel && sel.scrollIntoView) sel.scrollIntoView({ block: "nearest" });
  }
  function runSearch() {
    var q = searchInput.value.trim().toLowerCase(); searchSel = 0;
    var words = q ? q.split(/\s+/) : [];
    if (!q) { searchResults = []; renderResults(words); return; }
    searchResults = searchIndex.filter(function (r) {
      var l = r.label.toLowerCase();
      return words.every(function (w) { return l.indexOf(w) >= 0; });
    });
    searchResults.sort(function (a, b) {
      var ea = a.key === q ? 0 : (a.key && a.key.indexOf(q) === 0 ? 1 : 2), eb = b.key === q ? 0 : (b.key && b.key.indexOf(q) === 0 ? 1 : 2);
      return ea - eb || a.kind - b.kind || a.label.length - b.label.length;
    });
    renderResults(words);
    live(plural(searchResults.length, "resultOne", "resultMany"));
  }
  function openSearch() {
    if (!searchBox) return;
    if (!searchIndex) buildIndex();
    searchReturn = doc.activeElement;
    closeDrawer(); hidePop();
    searchBox.classList.add("open"); searchInput.value = ""; searchResults = []; renderResults([]);
    searchInput.focus();
  }
  function closeSearch(restore) {
    if (!searchOpen()) return;
    searchBox.classList.remove("open");
    if (restore !== false && searchReturn && searchReturn.focus) searchReturn.focus();
    searchReturn = null;
  }
  if (has("search")) {
    searchBox = el("div"); searchBox.id = "search"; searchBox.setAttribute("role", "dialog");
    searchBox.setAttribute("aria-modal", "true"); searchBox.setAttribute("aria-label", say("searchThisPage"));
    var box = el("div", "box");
    searchInput = el("input"); searchInput.type = "search"; searchInput.setAttribute("role", "combobox");
    searchInput.setAttribute("aria-label", say("search")); searchInput.setAttribute("aria-controls", "search-results");
    searchInput.setAttribute("aria-expanded", "false"); searchInput.setAttribute("aria-autocomplete", "list");
    searchInput.autocomplete = "off";
    searchInput.placeholder = idCore ? say("searchPlaceholderId", { example: prefixes[prefixes.length - 1] + "12" }) : say("searchPlaceholder");
    searchList = el("ol"); searchList.id = "search-results"; searchList.setAttribute("role", "listbox"); searchList.setAttribute("aria-label", say("results"));
    var hint = el("div", "hint", say("searchHint"));
    box.appendChild(searchInput); box.appendChild(searchList); box.appendChild(hint); searchBox.appendChild(box); root.appendChild(searchBox);
    searchInput.addEventListener("input", runSearch);
    searchInput.addEventListener("keydown", function (ev) {
      var n = Math.min(searchResults.length, T.SEARCH_MAX_ROWS);
      if (ev.key === "ArrowDown" && n) { searchSel = Math.min(searchSel + 1, n - 1); renderResults(searchInput.value.trim().toLowerCase().split(/\s+/)); ev.preventDefault(); }
      else if (ev.key === "ArrowUp" && n) { searchSel = Math.max(searchSel - 1, 0); renderResults(searchInput.value.trim().toLowerCase().split(/\s+/)); ev.preventDefault(); }
      else if (ev.key === "Enter" && searchResults[searchSel]) { var id = searchResults[searchSel].id; closeSearch(false); jump(id); ev.preventDefault(); }
      else if (ev.key === "Tab") ev.preventDefault();                 // the input is the only stop in the dialog
    });
    searchBox.addEventListener("click", function (ev) { if (ev.target === searchBox) closeSearch(); });
    if (searchBtn) searchBtn.addEventListener("click", openSearch);
    doc.addEventListener("keydown", function (ev) {
      var tg = ev.target || {}, typing = /^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName || "") || tg.isContentEditable;
      if (ev.key === "Escape") { closeSearch(); return; }
      if ((ev.key === "k" || ev.key === "K") && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); if (searchOpen()) closeSearch(); else openSearch(); return; }
      if (has("slash") && ev.key === "/" && !typing && !ev.ctrlKey && !ev.metaKey && !ev.altKey && !searchOpen()) { ev.preventDefault(); openSearch(); }
    });
  }
  doc.addEventListener("keydown", function (ev) { if (ev.key === "Escape") hidePop(); });

  /* ---------- Figures: bar, viewer, node popovers, edge highlight, figure index ---------- */
  var figN = 0, userMoved = false, viewer = null, vs = { s: 1, x: 0, y: 0 }, vInner = null, vStage = null, vReturn = null;
  ["wheel", "touchstart", "keydown", "mousedown"].forEach(function (e) {
    window.addEventListener(e, function () { userMoved = true; }, { passive: true, once: true });
  });
  var tipOf = {}, termNames = [], termRx = [];
  function buildTips() {
    tipOf = {};
    qsa("a.ref[data-tip][href^='#def-'], a.term[data-tip]", main).forEach(function (a) {
      var key = a.classList.contains("term") ? a.getAttribute("data-tip").split(T.POP_TIP_SEP)[0] : tokenOf(a.getAttribute("href")).slice(4);
      if (!tipOf[key]) tipOf[key] = { tip: a.getAttribute("data-tip"), href: a.getAttribute("href") };
    });
    termNames = Object.keys(tipOf).filter(function (k) { return !isId(k); }).sort(function (a, b) { return b.length - a.length; });
    termRx = termNames.map(function (k) { return new RegExp("(^|\\W)" + esc(k) + "(?:s|es)?(\\W|$)"); });
  }
  function captionOf(div) {
    var own = div.getAttribute("data-caption");
    if (own) return own;
    var p = div.previousElementSibling, s = p && p.querySelector && p.querySelector("strong");
    return s && p.textContent.indexOf(s.textContent) === 0 ? s.textContent.replace(/[.:]\s*$/, "").replace(CAPTION_PREFIX, "") : "";
  }
  function wireNodes(div, svg) {
    svg.addEventListener("dblclick", function () { openViewer(svg, div.__title || say("figureShort")); });
    qsa("g.node, g.actor, g.stateGroup, g.statediagram-state", svg).forEach(function (g) {
      var txt = (g.textContent || "").replace(/\s+/g, " ").trim(), hit = null, m = idFind ? txt.match(idFind) : null;
      if (m && tipOf[m[2]]) hit = tipOf[m[2]];
      if (!hit) for (var k = 0; k < termRx.length; k++) { if (termRx[k].test(txt)) { hit = tipOf[termNames[k]]; break; } }
      var name = (g.id || "").match(/^flowchart-(.+)-\d+$/);
      if (hit && has("popover")) {
        g.setAttribute("data-tip", hit.tip); g.setAttribute("data-href", hit.href);
        g.setAttribute("tabindex", "0"); g.setAttribute("role", "link"); g.classList.add("hasdef");
        g.setAttribute("aria-label", say("nodeLink", { text: txt }));
        g.addEventListener("click", function (ev) { ev.stopPropagation(); hidePop(); jump(tokenOf(hit.href)); });
        g.addEventListener("keydown", function (ev) { if (ev.key === "Enter") { hidePop(); jump(tokenOf(hit.href)); } });
        g.addEventListener("focus", function () { showPop(g); });
        g.addEventListener("blur", laterHide);
      }
      g.addEventListener("pointerenter", function (ev) {
        if (hit && has("popover") && ev.pointerType !== "touch") showPop(g);
        if (name) {
          svg.classList.add("dim"); g.classList.add("hi");
          var rx = new RegExp("^L[-_]" + esc(name[1]) + "[-_]|[-_]" + esc(name[1]) + "[-_]\\d+$");
          qsa("path", svg).forEach(function (p) { var pid = p.id || p.getAttribute("data-id") || ""; if (pid.charAt(0) === "L" && rx.test(pid)) p.classList.add("hi"); });
        }
      });
      g.addEventListener("pointerleave", function () {
        if (hit && has("popover")) laterHide();
        svg.classList.remove("dim"); qsa(".hi", svg).forEach(function (h) { h.classList.remove("hi"); });
      });
    });
  }
  function setSmallHint(div, svg) {
    var bar = div.querySelector(".figbar"); if (!bar) return;
    var vb = (svg.getAttribute("viewBox") || "").split(/\s+/).map(Number), w = svg.getBoundingClientRect().width;
    var small = vb.length === 4 && vb[2] > 0 && w > 0 && w / vb[2] < T.SMALL_TEXT_RATIO;
    var hint = bar.querySelector(".figbtn.small");
    if (small && !hint) {
      hint = el("button", "figbtn small", say("textSmall")); hint.type = "button";
      hint.addEventListener("click", function () { openViewer(div.__svg, div.__title || say("figureShort")); });
      bar.insertBefore(hint, bar.querySelector(".figbtn"));
    } else if (!small && hint) bar.removeChild(hint);
  }
  function enhance(div) {
    var svg = div.querySelector("svg");
    if (!svg) return;
    if (!div.getAttribute("data-enhanced")) {
      div.setAttribute("data-enhanced", "1");
      figN++;
      var n = figN, title = say("figure") + n, cap = captionOf(div);
      if (!div.id) div.id = "figure-" + n;
      div.__title = title + (cap ? " · " + cap : "");
      var bar = el("div", "figbar");
      var no = el("a", "figno", div.__title); no.href = "#" + div.id;
      var exp = el("button", "figbtn", say("expand")); exp.type = "button"; exp.setAttribute("aria-label", say("openFull", { title: title }));
      var lnk = el("button", "figbtn", say("copyLink")); lnk.type = "button";
      lnk.addEventListener("click", function () { copyText(location.href.split("#")[0] + "#" + div.id, lnk, say("copyLink")); });
      exp.addEventListener("click", function () { openViewer(div.__svg, div.__title); });
      bar.appendChild(no); bar.appendChild(exp); bar.appendChild(lnk);
      div.insertBefore(bar, div.firstChild);
    }
    if (div.__svg !== svg) { div.__svg = svg; wireNodes(div, svg); }      // also after a theme re-render
    setSmallHint(div, svg);
  }
  var figSignature = "";
  function figureIndex() {
    if (!nav || !menuList) return;
    var figs = qsa(".diagram[data-enhanced]", main);
    var sig = figs.map(function (d) { return d.id + (d.__title || ""); }).join("|");
    if (sig === figSignature) return;
    figSignature = sig;
    if (!figs.length) { if (figList && figList.parentNode.parentNode) figList.parentNode.parentNode.removeChild(figList.parentNode); figList = null; return; }
    if (!figList) {
      var li = el("li"), a = el("button", "navdoc navtoggle", say("figures")); a.type = "button"; a.setAttribute("aria-expanded", "false");
      figList = el("ul"); figList.hidden = true;
      a.addEventListener("click", function () { figList.hidden = !figList.hidden; a.setAttribute("aria-expanded", figList.hidden ? "false" : "true"); });
      li.appendChild(a); li.appendChild(figList); menuList.appendChild(li);
    }
    figList.textContent = "";
    figs.forEach(function (d) {
      var it = el("li"), a = el("a", null, d.__title || say("figureShort")); a.href = "#" + d.id; it.appendChild(a); figList.appendChild(it);
    });
  }
  function enhanceAll() {
    if (!has("figures")) return;
    if (!Object.keys(tipOf).length) buildTips();
    qsa(".diagram", main).forEach(enhance);
    figureIndex();
    if (!userMoved && location.hash) {
      var t0 = byId(tokenOf(location.hash)); if (t0) t0.scrollIntoView({ block: "start" });
    }
  }
  /* Full screen viewer: wheel and buttons zoom, drag pans, pinch zooms, double-click fits, Esc closes */
  function applyView() { if (vInner) vInner.style.transform = "translate(" + vs.x + "px," + vs.y + "px) scale(" + vs.s + ")"; }
  function fitView() {
    if (!vInner) return;
    var r = vStage.getBoundingClientRect(), c = vInner.firstChild;
    var w = (c.width && c.width.baseVal && c.width.baseVal.value) || 800, h = (c.height && c.height.baseVal && c.height.baseVal.value) || 600;
    vs.s = Math.min(r.width / w, r.height / h) * T.FIT_FILL; vs.x = (r.width - w * vs.s) / 2; vs.y = (r.height - h * vs.s) / 2; applyView();
  }
  function zoomAt(cx, cy, z) {
    var ns = Math.min(T.ZOOM_MAX, Math.max(T.ZOOM_MIN, vs.s * z)), k = ns / vs.s;
    vs.x = cx - (cx - vs.x) * k; vs.y = cy - (cy - vs.y) * k; vs.s = ns; applyView();
  }
  function openViewer(svg, title) {
    if (!viewer || !svg) return;
    vReturn = doc.activeElement;
    vStage.textContent = ""; vInner = el("div", "vinner");
    var c = svg.cloneNode(true); c.removeAttribute("style"); c.classList.remove("dim");
    qsa(".hi, .hasdef", c).forEach(function (x) { x.classList.remove("hi"); });
    var vb = (svg.getAttribute("viewBox") || "").split(/\s+/).map(Number), bb = svg.getBoundingClientRect();
    c.setAttribute("width", vb.length === 4 ? vb[2] : bb.width); c.setAttribute("height", vb.length === 4 ? vb[3] : bb.height);
    vInner.appendChild(c); vStage.appendChild(vInner);
    viewer.querySelector(".vt").textContent = title || say("figureShort");
    viewer.classList.add("open"); doc.body.style.overflow = "hidden";
    requestAnimationFrame(fitView); viewer.querySelector("[data-close]").focus();
  }
  function closeViewer() {
    if (!viewer || !viewer.classList.contains("open")) return;
    viewer.classList.remove("open"); vStage.textContent = ""; vInner = null; doc.body.style.overflow = "";
    if (vReturn && vReturn.focus) vReturn.focus();
  }
  if (has("figures")) {
    viewer = el("div"); viewer.id = "viewer"; viewer.setAttribute("role", "dialog"); viewer.setAttribute("aria-modal", "true"); viewer.setAttribute("aria-label", say("figureViewer"));
    viewer.innerHTML = '<div class="vbar"><span class="vt"></span><span class="vh"></span>' +
      '<button type="button" data-z="1.25"></button><button type="button" data-z="0.8"></button>' +
      '<button type="button" data-z="0"></button><button type="button" data-close="1"></button></div><div class="vstage"></div>';
    viewer.querySelector(".vh").textContent = say("viewerHint");
    viewer.querySelector('[data-z="1.25"]').textContent = say("zoomIn");
    viewer.querySelector('[data-z="0.8"]').textContent = say("zoomOut");
    viewer.querySelector('[data-z="0"]').textContent = say("fit");
    viewer.querySelector("[data-close]").textContent = say("closeViewer");
    root.appendChild(viewer);
    vStage = viewer.querySelector(".vstage");
    viewer.addEventListener("click", function (ev) {
      var b = ev.target.closest && ev.target.closest("button"); if (!b) return;
      if (b.hasAttribute("data-close")) return closeViewer();
      var z = Number(b.getAttribute("data-z"));
      if (!z) return fitView();
      var r = vStage.getBoundingClientRect(); zoomAt(r.width / 2, r.height / 2, z === 1.25 ? T.BUTTON_STEP : 1 / T.BUTTON_STEP);
    });
    vStage.addEventListener("wheel", function (ev) {
      ev.preventDefault();
      var r = vStage.getBoundingClientRect(); zoomAt(ev.clientX - r.left, ev.clientY - r.top, ev.deltaY < 0 ? T.WHEEL_STEP : 1 / T.WHEEL_STEP);
    }, { passive: false });
    var pointers = {}, pinch = 0, drag = null;
    vStage.addEventListener("pointerdown", function (ev) {
      pointers[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
      vStage.setPointerCapture(ev.pointerId); vStage.style.cursor = "grabbing";
      drag = { x: ev.clientX - vs.x, y: ev.clientY - vs.y }; pinch = 0;
    });
    vStage.addEventListener("pointermove", function (ev) {
      if (!pointers[ev.pointerId]) return;
      pointers[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
      var ids = Object.keys(pointers);
      if (ids.length === 2) {
        var p1 = pointers[ids[0]], p2 = pointers[ids[1]], d = Math.hypot(p1.x - p2.x, p1.y - p2.y), r = vStage.getBoundingClientRect();
        if (pinch) zoomAt((p1.x + p2.x) / 2 - r.left, (p1.y + p2.y) / 2 - r.top, d / pinch);
        pinch = d; return;
      }
      if (drag) { vs.x = ev.clientX - drag.x; vs.y = ev.clientY - drag.y; applyView(); }
    });
    var endPointer = function (ev) { delete pointers[ev.pointerId]; pinch = 0; drag = null; if (!Object.keys(pointers).length) vStage.style.cursor = ""; };
    vStage.addEventListener("pointerup", endPointer); vStage.addEventListener("pointercancel", endPointer);
    vStage.addEventListener("dblclick", fitView);
    viewer.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape") { closeViewer(); ev.stopPropagation(); return; }
      var r = vStage.getBoundingClientRect();
      if (ev.key === "+" || ev.key === "=") zoomAt(r.width / 2, r.height / 2, T.BUTTON_STEP);
      else if (ev.key === "-") zoomAt(r.width / 2, r.height / 2, 1 / T.BUTTON_STEP);
      else if (ev.key === "0") fitView();
      else if (ev.key === "Tab") {
        var items = qsa("button", viewer), i = items.indexOf(doc.activeElement);
        if (ev.shiftKey && i <= 0) { items[items.length - 1].focus(); ev.preventDefault(); }
        else if (!ev.shiftKey && i === items.length - 1) { items[0].focus(); ev.preventDefault(); }
      }
    });
    doc.addEventListener("keydown", function (ev) { if (ev.key === "Escape") closeViewer(); });
    var mo = new MutationObserver(function () { clearTimeout(mo.t); mo.t = setTimeout(enhanceAll, T.ENHANCE_DEBOUNCE_MS); });
    mo.observe(main, { childList: true, subtree: true });
    window.addEventListener("load", function () { setTimeout(enhanceAll, T.ENHANCE_LOAD_MS); });
    onTabChange.push(function () { setTimeout(enhanceAll, 0); });
    setTimeout(enhanceAll, 0);
  }

  /* ---------- Initial hash: reveal its tab and mark it ---------- */
  var h0 = tokenOf(location.hash);
  if (h0) { var t0 = reveal(h0); if (t0) { markTarget(t0); setTimeout(function () { t0.scrollIntoView({ block: "start" }); }, 0); } }

  /* Test hook for checks: window.__reader = { jump, openSearch, features } */
  window.__reader = { jump: jump, openSearch: openSearch, features: enabled, autolinked: function () { return autolinked; } };
})();
