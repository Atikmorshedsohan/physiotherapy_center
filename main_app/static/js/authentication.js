document.addEventListener("DOMContentLoaded", function () {
  const registerBox = document.getElementById("registerBox");
  const showRegisterForm = document.getElementById("showRegisterForm");

  showRegisterForm.addEventListener("click", function (e) {
    e.preventDefault();
    registerBox.style.display = "block";
    window.scrollTo({ top: registerBox.offsetTop, behavior: "smooth" });
  });
});
