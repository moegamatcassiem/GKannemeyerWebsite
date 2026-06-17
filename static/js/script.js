// Mobile nav toggle
const navToggle = document.querySelector(".nav-toggle");
const nav = document.querySelector(".nav");

if (navToggle && nav) {
  navToggle.addEventListener("click", () => {
    nav.classList.toggle("is-open");
  });

  // close mobile menu after tapping a link
  nav.querySelectorAll(".nav-mobile-panel a").forEach((link) => {
    link.addEventListener("click", () => nav.classList.remove("is-open"));
  });
}

// Gallery filtering
const filterButtons = document.querySelectorAll(".filter-btn");
const galleryItems = document.querySelectorAll(".gallery-item");

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const category = button.dataset.filter;

    filterButtons.forEach((b) => b.classList.remove("is-active"));
    button.classList.add("is-active");

    galleryItems.forEach((item) => {
      const matches = category === "all" || item.dataset.category === category;
      item.classList.toggle("is-hidden", !matches);
    });
  });
});

// Subtle scroll reveal
const revealEls = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window && revealEls.length) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.15 }
  );

  revealEls.forEach((el) => observer.observe(el));
} else {
  // fallback: just show everything
  revealEls.forEach((el) => el.classList.add("is-visible"));
}
