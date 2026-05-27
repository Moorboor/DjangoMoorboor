(function () {
  const root = document.getElementById("productCarousel");
  if (!root) return;

  const track = root.querySelector(".carousel-track");
  const viewport = root.querySelector(".carousel-viewport");
  const slides = Array.from(root.querySelectorAll(".carousel-slide"));
  const prevBtn = root.querySelector(".prev");
  const nextBtn = root.querySelector(".next");

  let index = 0;

  function slidesPerView() {
    if (window.matchMedia("(max-width: 768px)").matches) return 1;
    if (window.matchMedia("(max-width: 1024px)").matches) return 3;
    return 4;
  }

  function maxIndex() {
    return Math.max(0, slides.length - slidesPerView());
  }

  function slideWidth() {
    return slides[0].getBoundingClientRect().width;
  }

  function goTo(n) {
    index = Math.max(0, Math.min(maxIndex(), n));
    track.style.transform = `translateX(-${index * slideWidth()}px)`;
    if (prevBtn) prevBtn.disabled = index <= 0;
    if (nextBtn) nextBtn.disabled = index >= maxIndex();
  }

  if (prevBtn) prevBtn.addEventListener("click", () => goTo(index - 1));
  if (nextBtn) nextBtn.addEventListener("click", () => goTo(index + 1));

  // Touch swipe
  let touchX = 0,
    touchY = 0,
    dragging = false;
  const SWIPE_THRESHOLD = 50;

  viewport.addEventListener("touchstart", (e) => {
    touchX = e.changedTouches[0].clientX;
    touchY = e.changedTouches[0].clientY;
    dragging = true;
  }, {passive: true});

  viewport.addEventListener("touchmove", (e) => {
    if (!dragging) return;
    if (Math.abs(e.changedTouches[0].clientY - touchY) > 
        Math.abs(e.changedTouches[0].clientX - touchX)) {
      dragging = false;
    }
  }, {passive: true});

  viewport.addEventListener("touchend", (e) => {
    if (!dragging) return;
    dragging = false;
    const diff = touchX - e.changedTouches[0].clientX;
    if (Math.abs(diff) >= SWIPE_THRESHOLD) {
      goTo(diff > 0 ? index + 1 : index - 1);
    }
  }, {passive: true});

  window.addEventListener("resize", () => goTo(index));
  goTo(0);
})();