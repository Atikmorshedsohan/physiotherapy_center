document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("profileForm");

  form.addEventListener("submit", (e) => {
    const ageField = document.getElementById("id_age");  // Django auto-generates ids as id_fieldname
    if (ageField && ageField.value && (ageField.value < 0 || ageField.value > 120)) {
      e.preventDefault();
      alert("Please enter a valid age between 0 and 120.");
      ageField.focus();
    }
  });
});
