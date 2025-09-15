let appointments = [];
let counter = 1;

function openModal() {
  document.getElementById("appointmentModal").style.display = "flex";
}

function closeModal() {
  document.getElementById("appointmentModal").style.display = "none";
}

function addAppointment() {
  const name = document.getElementById("patientName").value;
  const date = document.getElementById("appointmentDate").value;
  const time = document.getElementById("appointmentTime").value;
  const status = document.getElementById("appointmentStatus").value;

  if (name && date && time) {
    appointments.push({ id: counter++, name, date, time, status });
    renderTable();
    closeModal();
    document.getElementById("patientName").value = "";
    document.getElementById("appointmentDate").value = "";
    document.getElementById("appointmentTime").value = "";
  } else {
    alert("Please fill all fields!");
  }
}

function deleteAppointment(id) {
  appointments = appointments.filter((app) => app.id !== id);
  renderTable();
}

function renderTable() {
  const tbody = document.getElementById("tableBody");
  tbody.innerHTML = "";
  appointments.forEach((app) => {
    const row = `
          <tr>
            <td>${app.id}</td>
            <td>${app.name}</td>
            <td>${app.date}</td>
            <td>${app.time}</td>
            <td>${app.status}</td>
            <td><button class="delete-btn" onclick="deleteAppointment(${app.id})">Delete</button></td>
          </tr>
        `;
    tbody.innerHTML += row;
  });
}

// Live search filter (bug fix: input and tbody now exist)
document.getElementById("search").addEventListener("keyup", function () {
  const value = this.value.toLowerCase();
  const rows = document.querySelectorAll("#appointmentsTable tbody tr");

  rows.forEach((row) => {
    const name = row.cells[1]?.innerText.toLowerCase() || "";
    row.style.display = name.includes(value) ? "" : "none";
  });
});
