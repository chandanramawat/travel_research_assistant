// ---------------------------------------------------------------------------
// Load real photos where they exist, keep the placeholder icon otherwise
// ---------------------------------------------------------------------------
document.querySelectorAll(".photo-thumb[data-src]").forEach((thumb) => {
  const src = thumb.dataset.src;
  const img = new Image();
  img.onload = () => {
    thumb.style.backgroundImage = `url("${src}")`;
    thumb.classList.add("loaded");
  };
  img.onerror = () => {
    // no file found yet — placeholder stays as-is
  };
  img.src = src;
});

// ---------------------------------------------------------------------------
// Filtering
// ---------------------------------------------------------------------------
const filterBtns = document.querySelectorAll(".filter-btn");
const cards = document.querySelectorAll(".photo-card");
const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");

filterBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    filterBtns.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    const filter = btn.dataset.filter;

    cards.forEach((card) => {
      const match = filter === "all" || card.dataset.trip === filter;
      card.style.display = match ? "" : "none";
    });

    sidebar.classList.remove("open");
  });
});

sidebarToggle.addEventListener("click", () => {
  sidebar.classList.toggle("open");
});

// ---------------------------------------------------------------------------
// Lightbox
// ---------------------------------------------------------------------------
const lightbox = document.getElementById("lightbox");
const lbFrame = document.getElementById("lbFrame");
const lbCaption = document.getElementById("lbCaption");
const lbClose = document.getElementById("lbClose");
const lbPrev = document.getElementById("lbPrev");
const lbNext = document.getElementById("lbNext");

let currentIndex = 0;

function visibleCards() {
  return Array.from(cards).filter((c) => c.style.display !== "none");
}

function openLightbox(index) {
  const list = visibleCards();
  if (!list.length) return;
  currentIndex = (index + list.length) % list.length;
  const card = list[currentIndex];
  const thumb = card.querySelector(".photo-thumb");
  const place = card.querySelector(".pc-place").textContent;
  const date = card.querySelector(".pc-date").textContent;

  lbFrame.style.backgroundImage = thumb.classList.contains("loaded")
    ? thumb.style.backgroundImage
    : "none";
  lbCaption.textContent = `${place} — ${date}`;
  lightbox.classList.add("open");
}

function closeLightbox() {
  lightbox.classList.remove("open");
}

cards.forEach((card, i) => {
  card.addEventListener("click", () => openLightbox(visibleCards().indexOf(card)));
});

lbClose.addEventListener("click", closeLightbox);
lightbox.addEventListener("click", (e) => {
  if (e.target === lightbox) closeLightbox();
});
lbPrev.addEventListener("click", () => openLightbox(currentIndex - 1));
lbNext.addEventListener("click", () => openLightbox(currentIndex + 1));

document.addEventListener("keydown", (e) => {
  if (!lightbox.classList.contains("open")) return;
  if (e.key === "Escape") closeLightbox();
  if (e.key === "ArrowLeft") openLightbox(currentIndex - 1);
  if (e.key === "ArrowRight") openLightbox(currentIndex + 1);
});