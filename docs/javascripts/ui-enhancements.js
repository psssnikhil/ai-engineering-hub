/* ============================================================
   AI Engineering Hub — Production UI Micro-interactions & Polish
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {
  // 1. Wrap tables in responsive container if not already wrapped
  const tables = document.querySelectorAll(".md-typeset table:not([class])");
  tables.forEach(function (table) {
    if (!table.parentElement.classList.contains("table-wrapper")) {
      const wrapper = document.createElement("div");
      wrapper.className = "table-wrapper";
      wrapper.style.overflowX = "auto";
      wrapper.style.webkitOverflowScrolling = "touch";
      wrapper.style.marginBottom = "1.5em";
      wrapper.style.borderRadius = "14px";
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }
  });

  // 2. Add search keyboard shortcut hint badge in header
  const searchInput = document.querySelector(".md-search__input");
  if (searchInput) {
    const isMac = navigator.platform.toUpperCase().indexOf("MAC") >= 0;
    const shortcutText = isMac ? "⌘K" : "Ctrl+K";
    searchInput.setAttribute("placeholder", `Search curriculum (${shortcutText})`);
  }

  // 3. Smooth scrolling for internal anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href').substring(1);
      if (targetId) {
        const targetElement = document.getElementById(targetId);
        if (targetElement) {
          e.preventDefault();
          targetElement.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });
});
