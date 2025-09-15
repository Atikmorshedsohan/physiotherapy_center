document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('registrationForm');

  form.addEventListener('submit', function (e) {
    const password1 = document.getElementById('id_password1');
    const password2 = document.getElementById('id_password2');

    if (password1 && password2 && password1.value !== password2.value) {
      e.preventDefault();
      alert("Passwords do not match!");
    }
  });
});
