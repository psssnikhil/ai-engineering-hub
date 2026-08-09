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

  // 4. LinkedIn link in the header, next to the GitHub source link.
  // Material only generates a repo link from `repo_url`; there's no
  // config option for a second header icon, so it's inserted here
  // rather than duplicating the whole header partial for one link.
  const headerSource = document.querySelector(".md-header__source");
  if (headerSource && !document.querySelector(".md-header__linkedin")) {
    const linkedin = document.createElement("a");
    linkedin.href = "https://www.linkedin.com/in/nikhilpentapalli/";
    linkedin.target = "_blank";
    linkedin.rel = "noopener";
    linkedin.title = "Connect on LinkedIn";
    linkedin.className = "md-header__linkedin";
    linkedin.innerHTML =
      '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" aria-hidden="true">' +
      '<path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.34V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.38-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.07 2.07 0 1 1 0-4.13 2.07 2.07 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45z"/>' +
      "</svg>";
    headerSource.parentNode.insertBefore(linkedin, headerSource);
  }

  // 5. Header scroll-shadow: toggle a class once the page scrolls past the
  // top so the header can pick up a stronger shadow (CSS can't observe
  // scroll position on its own — this is the one bit of header behavior
  // the new template override needs from JS).
  const header = document.querySelector(".md-header");
  if (header) {
    const toggleScrolled = () => {
      header.classList.toggle("md-header--scrolled", window.scrollY > 8);
    };
    toggleScrolled();
    window.addEventListener("scroll", toggleScrolled, { passive: true });
  }
});
