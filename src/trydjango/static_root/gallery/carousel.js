class CategoryCarousel {
  constructor(cardElement) {
    this.card = cardElement;
    this.carousel = cardElement.querySelector('.carousel');
    this.slides = cardElement.querySelectorAll('.carousel-slide');
    this.dots = cardElement.querySelectorAll('.dot');
    this.currentSlide = 0;
    this.interval = null;

    if (this.slides.length > 0) {
      this.init();
    }
  }

  init() {
    // Show first slide
    this.showSlide(0);

    // Auto-rotate slides every 3 seconds
    this.interval = setInterval(() => {
      this.nextSlide();
    }, 3000);

    // Handle dot clicks
    this.dots.forEach((dot, index) => {
      dot.addEventListener('click', () => {
        clearInterval(this.interval);
        this.showSlide(index);
        this.restartInterval();
      });
    });

    // Pause on hover
    this.carousel.addEventListener('mouseenter', () => {
      clearInterval(this.interval);
    });

    this.carousel.addEventListener('mouseleave', () => {
      this.restartInterval();
    });
  }

  showSlide(index) {
    // Remove active class from all slides and dots
    this.slides.forEach(slide => slide.classList.remove('active'));
    this.dots.forEach(dot => dot.classList.remove('active'));

    // Add active class to current slide and dot
    this.slides[index].classList.add('active');
    this.dots[index].classList.add('active');

    this.currentSlide = index;
  }

  nextSlide() {
    const next = (this.currentSlide + 1) % this.slides.length;
    this.showSlide(next);
  }

  restartInterval() {
    this.interval = setInterval(() => {
      this.nextSlide();
    }, 3000);
  }
}

// Initialize all carousels on page load
document.addEventListener('DOMContentLoaded', () => {
  const categoryCards = document.querySelectorAll('.category-card');
  categoryCards.forEach(card => new CategoryCarousel(card));
});