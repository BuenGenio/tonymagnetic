document.documentElement.classList.add("js");

const header = document.querySelector(".site-header");
const menuButton = document.querySelector(".menu-toggle");
const navigation = document.querySelector(".primary-nav");

function setMenu(open) {
  if (!menuButton || !navigation) return;
  menuButton.setAttribute("aria-expanded", String(open));
  menuButton.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  navigation.classList.toggle("is-open", open);
  document.body.classList.toggle("menu-open", open);
  if (open) requestAnimationFrame(() => navigation.querySelector("a")?.focus());
}

menuButton?.addEventListener("click", () => {
  setMenu(menuButton.getAttribute("aria-expanded") !== "true");
});

navigation?.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => setMenu(false));
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menuButton?.getAttribute("aria-expanded") === "true") {
    setMenu(false);
    menuButton.focus();
  }
});

function updateHeader() {
  header?.classList.toggle("is-scrolled", window.scrollY > 24);
}

updateHeader();
window.addEventListener("scroll", updateHeader, { passive: true });

if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { rootMargin: "0px 0px -8%", threshold: 0.08 });

  document.querySelectorAll("[data-reveal]").forEach((el) => observer.observe(el));
} else {
  document.querySelectorAll("[data-reveal]").forEach((el) => el.classList.add("is-visible"));
}

/* ------------------------------------------------------------ chapters ---
   The chapters section renders in one of several view modes, chosen with the
   .view-switch and stored on the section as data-view (CSS does the layout).
   Chapters with more than one slide get dots and, in slideshow mode, a gentle
   auto-advance that only runs while the panel is on screen. */

const VIEW_KEY = "chapters-view";
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

document.querySelectorAll(".chapters[data-view]").forEach((section) => {
  const buttons = [...section.querySelectorAll("[data-view-choice]")];
  const known = buttons.map((b) => b.dataset.viewChoice);

  function apply(view, persist) {
    section.dataset.view = view;
    buttons.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.viewChoice === view)));
    if (persist) {
      try { localStorage.setItem(VIEW_KEY, view); } catch (_) { /* private mode */ }
    }
    section.dispatchEvent(new CustomEvent("chapters:view"));
  }

  let saved = null;
  try { saved = localStorage.getItem(VIEW_KEY); } catch (_) { /* private mode */ }
  apply(known.includes(saved) ? saved : section.dataset.view, false);
  buttons.forEach((b) => b.addEventListener("click", () => apply(b.dataset.viewChoice, true)));
});

document.querySelectorAll(".chapter-media").forEach((media) => {
  const slides = [...media.querySelectorAll(".slide")];
  if (slides.length < 2) return;
  const section = media.closest(".chapters");
  let index = Math.max(0, slides.findIndex((s) => s.classList.contains("is-active")));

  const nav = document.createElement("div");
  nav.className = "slide-nav";
  nav.setAttribute("role", "group");
  nav.setAttribute("aria-label", "Photos");
  const dots = slides.map((_, i) => {
    const dot = document.createElement("button");
    dot.type = "button";
    dot.setAttribute("aria-label", `Photo ${i + 1} of ${slides.length}`);
    dot.addEventListener("click", (event) => {
      event.preventDefault();
      show(i);
      restart();
    });
    nav.append(dot);
    return dot;
  });
  media.append(nav);

  function show(i) {
    index = (i + slides.length) % slides.length;
    slides.forEach((s, j) => s.classList.toggle("is-active", j === index));
    dots.forEach((d, j) => d.setAttribute("aria-current", j === index ? "true" : "false"));
  }

  let timer = null;
  let onScreen = false;
  let held = false;                        // hovered or focused — don't move under the reader

  function update() {
    const run = onScreen && !held && !document.hidden && !reduceMotion
      && (!section || section.dataset.view === "slideshow");
    if (run && !timer) timer = setInterval(() => show(index + 1), 5200);
    if (!run && timer) { clearInterval(timer); timer = null; }
  }
  function restart() {
    if (timer) { clearInterval(timer); timer = null; }
    update();
  }

  new IntersectionObserver(([entry]) => {
    onScreen = entry.isIntersecting;
    update();
  }, { threshold: 0.35 }).observe(media);

  const panel = media.closest(".chapter, .page-heading") || media;
  panel.addEventListener("pointerenter", () => { held = true; update(); });
  panel.addEventListener("pointerleave", () => { held = false; update(); });
  panel.addEventListener("focusin", () => { held = true; update(); });
  panel.addEventListener("focusout", () => { held = false; update(); });
  section?.addEventListener("chapters:view", update);
  document.addEventListener("visibilitychange", update);

  show(index);
});
