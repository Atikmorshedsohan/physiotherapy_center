// Smooth scroll to review section
function scrollToBooking() {
  document.getElementById("review-section").scrollIntoView({ behavior: "smooth" });
}

// Fade-in effect for review card when visible
document.addEventListener("DOMContentLoaded", () => {
  const reviewCard = document.querySelector(".review-card");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          reviewCard.classList.add("visible");
        }
      });
    },
    { threshold: 0.2 }
  );
  observer.observe(reviewCard);
});
