/* PELIVET — shared client-side behaviour */
(function () {
  "use strict";

  // Year in footer
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Sticky nav shadow
  var nav = document.getElementById("nav");
  if (nav) {
    var onScroll = function () { nav.classList.toggle("scrolled", window.scrollY > 12); };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // Mobile menu
  var ham = document.getElementById("hamburger");
  var menu = document.getElementById("mobileMenu");
  if (ham && menu) {
    ham.addEventListener("click", function () {
      var open = menu.style.display === "flex";
      menu.style.display = open ? "none" : "flex";
      ham.setAttribute("aria-expanded", String(!open));
    });
    menu.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        menu.style.display = "none";
        ham.setAttribute("aria-expanded", "false");
      });
    });
  }

  // Scroll reveal
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });
    reveals.forEach(function (el, i) {
      el.style.transitionDelay = (i % 4 * 0.06) + "s";
      io.observe(el);
    });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  // Dismissable flash messages (auto-hide after 6s)
  document.querySelectorAll(".flash").forEach(function (f) {
    var close = function () { f.style.display = "none"; };
    var x = f.querySelector(".x");
    if (x) x.addEventListener("click", close);
    setTimeout(close, 6000);
  });

  // Date inputs can't be in the past
  document.querySelectorAll('input[type="date"]').forEach(function (d) {
    if (!d.min) d.min = new Date().toISOString().split("T")[0];
  });
})();
