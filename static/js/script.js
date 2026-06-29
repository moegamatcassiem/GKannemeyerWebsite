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
const showMoreBtn = document.getElementById("show-more-btn");
const overlay = document.querySelector("#lightbox-overlay");
const lightboxImg = document.querySelector("#lightbox-img");
const closeBtn = document.querySelector("#lightbox-close");

let visibleCount = 6; // initial number of visible items

function updateGallery() {
  const activeFilter = document.querySelector(".filter-btn.is-active");
  const category = activeFilter ? activeFilter.dataset.filter : "all";
  let matchCount = 0;

  galleryItems.forEach((item) => {
    const matches = category === "all" || item.dataset.category === category;
    if (matches) {
      matchCount++;
      item.classList.toggle("is-hidden", matchCount > visibleCount);
    } else {
      item.classList.add("is-hidden");
    }
  });

  showMoreBtn.style.display = matchCount > visibleCount ? "block" : "none";
}

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    filterButtons.forEach((b) => b.classList.remove("is-active"));
    button.classList.add("is-active");
    visibleCount = 6; // reset visible count when changing filter

    updateGallery();
  });
});

galleryItems.forEach((item) => {
  item.addEventListener("click", () => {
    const img = item.querySelector("img");
    if (img) {
      lightboxImg.src = img.src;
      overlay.classList.add("is-active");
    }
  });
});

closeBtn.addEventListener("click", () => {
  overlay.classList.remove("is-active");
});

overlay.addEventListener("click", (e) => {
  if (e.target === overlay) {
    overlay.classList.remove("is-active");
  }
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    overlay.classList.remove("is-active");
  }
});

showMoreBtn.addEventListener("click", () => {
  visibleCount += 6;
  updateGallery();
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

updateGallery();
