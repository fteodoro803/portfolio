// Site-wide behaviour: the light/dark toggle and the Other Projects dialogs.
(function () {
  var root = document.documentElement;

  var toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var current = root.dataset.theme ||
        (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      var next = current === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("fte-theme", next); } catch (e) {}
    });
  }

  document.querySelectorAll("[data-open]").forEach(function (button) {
    var dialog = document.getElementById(button.dataset.open);
    if (!dialog || typeof dialog.showModal !== "function") return;
    button.addEventListener("click", function () { dialog.showModal(); });
  });

  // Clicking the dimmed area outside a dialog closes it.
  document.querySelectorAll("dialog.project-dialog").forEach(function (dialog) {
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });
  });
})();
