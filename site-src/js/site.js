// Site-wide behaviour: the light/dark toggle, the project pop-ups and the card picture carousels.
(function () {
  var root = document.documentElement;

  var toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var next = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("fte-theme", next); } catch (e) {}
    });
  }

  document.querySelectorAll("[data-open]").forEach(function (button) {
    var dialog = document.getElementById(button.dataset.open);
    if (!dialog || typeof dialog.showModal !== "function") return;
    button.addEventListener("click", function () { dialog.showModal(); });
  });

  // Card pictures: arrows and dots scroll the row of slides, wrapping at the ends.
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  document.querySelectorAll("[data-carousel]").forEach(function (media) {
    var track = media.querySelector(".media-track");
    var dots = media.querySelectorAll(".media-dot");
    var count = dots.length;
    var current = 0;

    function show(index) {
      current = (index + count) % count;
      track.scrollTo({ left: current * track.clientWidth, behavior: reduceMotion.matches ? "auto" : "smooth" });
      dots.forEach(function (dot, i) {
        if (i === current) dot.setAttribute("aria-current", "true");
        else dot.removeAttribute("aria-current");
      });
    }

    media.querySelector(".prev").addEventListener("click", function () { show(current - 1); });
    media.querySelector(".next").addEventListener("click", function () { show(current + 1); });
    dots.forEach(function (dot) {
      dot.addEventListener("click", function () { show(Number(dot.dataset.slide)); });
    });
    // The card can be resized (rotating a phone), so keep the visible slide lined up.
    window.addEventListener("resize", function () { track.scrollLeft = current * track.clientWidth; });
    show(0);
  });

  // Home page showcase: one project at a time. Without this script they all show in a column.
  document.querySelectorAll("[data-showcase]").forEach(function (showcase) {
    var slides = showcase.querySelectorAll(".showcase-slide");
    var thumbs = showcase.querySelectorAll(".showcase-thumb");
    var current = 0;
    if (slides.length < 2) return;

    function show(index) {
      current = (index + slides.length) % slides.length;
      slides.forEach(function (slide, i) { slide.hidden = i !== current; });
      thumbs.forEach(function (thumb, i) {
        if (i === current) thumb.setAttribute("aria-current", "true");
        else thumb.removeAttribute("aria-current");
      });
      // A picture carousel inside a hidden slide lost its position, so line them up again.
      window.dispatchEvent(new Event("resize"));
    }

    showcase.querySelectorAll(".showcase-nav, .showcase-thumbs").forEach(function (el) { el.hidden = false; });
    showcase.querySelectorAll(".showcase-arrow.prev").forEach(function (b) { b.addEventListener("click", function () { show(current - 1); }); });
    showcase.querySelectorAll(".showcase-arrow.next").forEach(function (b) { b.addEventListener("click", function () { show(current + 1); }); });
    thumbs.forEach(function (thumb, i) { thumb.addEventListener("click", function () { show(i); }); });
    show(0);
  });

  // Clicking the dimmed area outside a dialog closes it.
  document.querySelectorAll("dialog.project-dialog").forEach(function (dialog) {
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });
  });
})();
