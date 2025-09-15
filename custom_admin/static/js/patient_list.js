function filterPatients() {
  let input = document.getElementById("searchInput").value.toLowerCase();
  let rows = document.querySelectorAll("#patientsTable tbody tr");

  rows.forEach(row => {
    let text = row.innerText.toLowerCase();
    if (text.includes(input)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
}
