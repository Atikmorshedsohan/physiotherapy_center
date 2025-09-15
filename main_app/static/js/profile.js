// profile.js
document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", function (e) {
      const confirmSave = confirm("Do you want to save the changes?");
      if (!confirmSave) {
        e.preventDefault();
      }
    });
  }

  // Fade-in effect for profile card
  const card = document.querySelector(".profile-card");
  if (card) {
    card.style.opacity = "0";
    setTimeout(() => {
      card.style.transition = "opacity 1s";
      card.style.opacity = "1";
    }, 200);
  }
});
