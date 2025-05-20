function toggleTheme() {
  const link = document.getElementById("theme-stylesheet");

  if (!link) return;

  const current = link.getAttribute("href");

  if (current.includes("GhostScript2v2.2.css")) {
    link.setAttribute("href", "styles/themes/TauAcademic.css");
  } else {
    link.setAttribute("href", "styles/themes/GhostScript2v2.2.css");
  }
}
