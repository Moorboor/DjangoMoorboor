(function () {
  const prevUrl = document.querySelector(".nav-btn.prev:not(.disabled)")?.href ?? null;
  const nextUrl = document.querySelector(".nav-btn.next:not(.disabled)")?.href ?? null;

  let startX = 0, startY = 0, dragX = 0;
  let active = false, axis = null, fromCarousel = false;
  const THRESHOLD = 0.35;

  document.addEventListener("touchstart", (e) => {
    fromCarousel = !!e.target.closest("#productCarousel");
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
    dragX = 0;
    active = true;
    axis = null;
  }, {passive: true});

  document.addEventListener("touchmove", (e) => {
    if (!active || fromCarousel) return;
    const dx = e.touches[0].clientX - startX;
    const dy = e.touches[0].clientY - startY;
    if (!axis) {
      if (Math.abs(dx) < 8 && Math.abs(dy) < 8) return;
      axis = Math.abs(dx) >= Math.abs(dy) ? "x" : "y";
      if (axis === "y") {
        active = false;
        return;
      }
    }
    let d = dx;
    if (d > 0 && !prevUrl) d = 0;
    if (d < 0 && !nextUrl) d = 0;
    dragX = d;
    document.body.style.transform = `translateX(${d}px)`;
  }, {passive: true});

  document.addEventListener("touchend", () => {
    if (!active || axis !== "x") {
      active = false;
      return;
    }
    active = false;
    const ratio = Math.abs(dragX) / window.innerWidth;
    if (dragX > 0 && ratio >= THRESHOLD && prevUrl) {
      window.location.href = prevUrl;
    } else if (dragX < 0 && ratio >= THRESHOLD && nextUrl) {
      window.location.href = nextUrl;
    } else {
      document.body.style.transform = "";
    }
    dragX = 0;
  }, {passive: true});
})();