/* MathJax configuration for MkDocs Material + pymdownx.arithmatex */
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true,
    packages: { "[+]": ["ams", "boldsymbol"] }
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

/* Re-typeset math after instant navigation */
document$.subscribe(function () {
  if (typeof MathJax !== "undefined" && MathJax.typesetPromise) {
    if (MathJax.startup && MathJax.startup.output) {
      MathJax.startup.output.clearCache();
    }
    MathJax.typesetClear();
    MathJax.typesetPromise();
  }
});

