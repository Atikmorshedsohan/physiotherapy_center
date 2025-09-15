let allDoctors = [];

// ==============================
// Load Doctors from Backend
// ==============================
async function loadDoctors() {
    try {
        const response = await fetch("/api/doctors/", { credentials: "include" });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        allDoctors = await response.json();
        renderDoctors(allDoctors);
    } catch (error) {
        console.error("Error fetching doctors:", error);
        document.getElementById("doctorList").innerHTML = "<p>Failed to load doctors.</p>";
    }
}

// ==============================
// Render Doctor Cards
// ==============================
function renderDoctors(list) {
    const container = document.getElementById("doctorList");
    container.innerHTML = "";

    if (list.length === 0) {
        container.innerHTML = "<p>No doctors found.</p>";
        return;
    }

    list.forEach(doc => {
        const card = document.createElement("div");
        card.classList.add("doctor-card");

        let availability = doc.availability;
        if (!availability) {
            availability = {};
        } else if (typeof availability === "string") {
            try {
                availability = JSON.parse(availability);
            } catch (e) {
                availability = {};
            }
        }

        let availabilityHtml = "<ul>";
        if (Object.keys(availability).length > 0) {
            for (const [day, time] of Object.entries(availability)) {
                availabilityHtml += `<li><strong>${day}:</strong> ${time}</li>`;
            }
        } else {
            availabilityHtml += "<li>No availability provided</li>";
        }
        availabilityHtml += "</ul>";

        card.innerHTML = `
            <h2>${doc.full_name}</h2>
            <p><strong>Specialization:</strong> ${doc.specialization}</p>
            <p><strong>Phone:</strong> ${doc.phone}</p>
            <p><strong>Email:</strong> ${doc.email}</p>
            <div><strong>Availability:</strong> ${availabilityHtml}</div>
            <button onclick="bookDoctor(${doc.id})">Book Now</button>
        `;

        container.appendChild(card);
    });
}

// ==============================
// Search Filter
// ==============================
function filterDoctors() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const filtered = allDoctors.filter(doc =>
        doc.full_name.toLowerCase().includes(input) ||
        doc.specialization.toLowerCase().includes(input)
    );
    renderDoctors(filtered);
}

// ==============================
// Suggestions Box
// ==============================
function showSuggestions() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const suggestionsBox = document.getElementById("suggestions");
    suggestionsBox.innerHTML = "";

    if (input.length === 0) {
        suggestionsBox.style.display = "none";
        renderDoctors(allDoctors);
        return;
    }

    const matches = allDoctors.filter(doc =>
        doc.full_name.toLowerCase().includes(input) ||
        doc.specialization.toLowerCase().includes(input)
    );

    matches.slice(0, 5).forEach(doc => {
        const suggestion = document.createElement("div");
        suggestion.classList.add("suggestion-item");
        suggestion.innerHTML = `<strong>${doc.full_name}</strong> <span>(${doc.specialization})</span>`;
        
        suggestion.onclick = () => {
            document.getElementById("searchInput").value = doc.full_name;
            suggestionsBox.style.display = "none";
            renderDoctors([doc]);
        };

        suggestionsBox.appendChild(suggestion);
    });

    suggestionsBox.style.display = matches.length > 0 ? "block" : "none";
}

// ==============================
// Modal Handling
// ==============================
function bookDoctor(doctorId) {
    const doctor = allDoctors.find(d => d.id === doctorId);
    if (doctor) {
        document.getElementById("doctorId").value = doctor.id;
        document.getElementById("appointmentModal").style.display = "flex";
    }
}

function closeModal() {
    document.getElementById("appointmentModal").style.display = "none";
}

// ==============================
// Form Submit (Book Appointment)
// ==============================
document.getElementById("appointmentForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const doctorId = document.getElementById("doctorId").value;
    const scheduledDate = document.getElementById("scheduledDate").value;
    const scheduledTime = document.getElementById("scheduledTime").value;

    if (!doctorId || !scheduledDate || !scheduledTime) {
        alert("Please fill in all fields.");
        return;
    }

    const formData = {
        doctor: doctorId,
        scheduled_date: scheduledDate,
        scheduled_time: scheduledTime,
        status: "Pending"
    };

    try {
        const response = await fetch("/api/appointments/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: JSON.stringify(formData),
            credentials: "include"   // ✅ send session cookie with request
        });

        const data = await response.json();

        if (response.ok && data.success) {
            alert("Appointment booked successfully!");
            closeModal();
        } else if (response.status === 403) {
            alert("Please login to book an appointment.");
            window.location.href = "/login/";
        } else {
            alert("Error: " + (data.error || "Something went wrong."));
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong.");
    }
});

// ==============================
// Helper: Get CSRF Token
// ==============================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ==============================
// Init
// ==============================
document.addEventListener("DOMContentLoaded", loadDoctors);
