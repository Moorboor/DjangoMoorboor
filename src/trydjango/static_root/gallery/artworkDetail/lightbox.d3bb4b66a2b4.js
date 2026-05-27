document.addEventListener("DOMContentLoaded", function () {
  const lightbox = document.getElementById("lightbox");
  const lbImg = document.getElementById("lightbox-img");
  const lbVideo = document.getElementById("lightbox-video");
  const lbVideoSrc = document.getElementById("lightbox-video-src");
  const lbClose = document.getElementById("lightbox-close");
  const lbPrev = document.getElementById("lightbox-prev");
  const lbNext = document.getElementById("lightbox-next");
  const lbCaption = document.getElementById("lightbox-caption");

  let images = [];
  let currentIndex = 0;

  function buildImageList() {
    images = [];

    const mainImg = document.querySelector("[data-main-image]");
    if (mainImg) {
      images.push({
        type: "image",
        src: mainImg.dataset.lightbox,
        alt: mainImg.alt,
        caption: "",
      });
    }

    document.querySelectorAll("#productCarousel .carousel-slide").forEach((slide) => {
      const img = slide.querySelector("[data-lightbox]");
      const vidBtn = slide.querySelector("[data-lightbox-video]");

      if (img) {
        images.push({
          type: "image",
          src: img.dataset.lightbox,
          alt: img.alt,
          caption: img.dataset.caption || "",
        });
      } else if (vidBtn) {
        images.push({
          type: "video",
          src: vidBtn.dataset.lightboxVideo,
          caption: vidBtn.dataset.caption || "",
        });
      }
    });
  }

  function openAt(index) {
    currentIndex = Math.max(0, Math.min(images.length - 1, index));
    const item = images[currentIndex];

    if (item.type === "video") {
      lbImg.style.display = "none";
      lbVideo.style.display = "block";
      lbVideoSrc.src = item.src;
      lbVideo.load();
    } else {
      lbVideo.pause();
      lbVideo.style.display = "none";
      lbImg.style.display = "block";
      lbImg.src = item.src;
      lbImg.alt = item.alt || "";
    }

    lbCaption.textContent = item.caption;
    lightbox.classList.add("open");
    document.body.style.overflow = "hidden";
    updateArrows();
  }

  function close() {
    lightbox.classList.remove("open");
    lbImg.src = "";
    lbVideo.pause();
    lbVideoSrc.src = "";
    lbVideo.load();
    lbCaption.textContent = "";
    document.body.style.overflow = "";
  }

  function updateArrows() {
    lbPrev.disabled = currentIndex <= 0;
    lbNext.disabled = currentIndex >= images.length - 1;
  }

  document.querySelector("[data-main-image]")?.addEventListener("click", () => {
    buildImageList();
    openAt(0);
  });

  document.getElementById("productCarousel")?.addEventListener("click", (e) => {
    const img = e.target.closest("[data-lightbox]");
    const vidBtn = e.target.closest("[data-lightbox-video]");
    if (!img && !vidBtn) return;

    buildImageList();

    const allSlides = Array.from(
      document.querySelectorAll("#productCarousel .carousel-slide")
    );
    const clickedSlide = (img || vidBtn).closest(".carousel-slide");
    const slideIndex = allSlides.indexOf(clickedSlide);
    openAt(slideIndex + 1);
  });

  lbPrev.addEventListener("click", (e) => {
    e.stopPropagation();
    openAt(currentIndex - 1);
  });
  lbNext.addEventListener("click", (e) => {
    e.stopPropagation();
    openAt(currentIndex + 1);
  });

  lightbox.addEventListener("click", (e) => {
    if (e.target === lightbox) close();
  });
  lbClose.addEventListener("click", close);

  document.addEventListener("keydown", (e) => {
    if (!lightbox.classList.contains("open")) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowLeft") openAt(currentIndex - 1);
    if (e.key === "ArrowRight") openAt(currentIndex + 1);
  });
});