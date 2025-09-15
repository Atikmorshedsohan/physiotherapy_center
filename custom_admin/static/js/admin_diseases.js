document.addEventListener("DOMContentLoaded", () => {
  const diseaseForm = document.getElementById("diseaseForm");

  if (diseaseForm) {
    diseaseForm.addEventListener("submit", async (e) => {
      e.preventDefault(); // stop full page reload

      const formData = new FormData(diseaseForm);

      const response = await fetch("", {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });

      const data = await response.json();

      // Show latest ID
      if (data.latest_id) {
        document.getElementById("latestIdBox").innerHTML =
          `<strong>Latest inserted ID:</strong> ${data.latest_id}`;
      }
    });
  }
});
