let allDoctors = [];
let isLoggedIn = false; // Track login status

// ==============================
// Check Login Status
// ==============================
async function checkLoginStatus() {
    try {
        const response = await fetch("/api/check-login/", { credentials: "include" });
        if (!response.ok) throw new Error("Not logged in");
        const data = await response.json();
        isLoggedIn = data.is_authenticated;
    } catch (error) {
        isLoggedIn = false;
    }
}

// ==============================
// Load Doctors from Backend
// ==============================
async function loadDoctors() {
    try {
        const response = await fetch("/api/doctors/", { credentials: "include" });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
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

        let availability = doc.availability || {};
        if (typeof availability === "string") {
            try { availability = JSON.parse(availability); } catch (e) { availability = {}; }
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

        // Button behavior based on login
        const bookButton = isLoggedIn
            ? `<button onclick="bookDoctor(${doc.id})">Book Now</button>`
            : `<button onclick="redirectToLogin()">Book Now</button>`;

        card.innerHTML = `
            <h2>${doc.full_name}</h2>
            <p><strong>Specialization:</strong> ${doc.specialization}</p>
            <p><strong>Phone:</strong> ${doc.phone}</p>
            <p><strong>Email:</strong> ${doc.email}</p>
            <div><strong>Availability:</strong> ${availabilityHtml}</div>
            ${bookButton}
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
// ==============================
// Book Doctor / Modal Handling
// ==============================
function bookDoctor(doctorId) {
    if (!isLoggedIn) {
        // Only alert once and redirect
        alert("Please login to book an appointment.");
        window.location.href = "/login/";
        return;
    }

    const doctor = allDoctors.find(d => d.id === doctorId);
    if (doctor) {
        document.getElementById("doctorId").value = doctor.id;
        document.getElementById("appointmentModal").style.display = "flex";
    }
}

// ==============================
// Form Submit (Book Appointment)
// ==============================
document.getElementById("appointmentForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    // Prevent submission if user is not logged in
    if (!isLoggedIn) {
        alert("Please login to book an appointment.");
        window.location.href = "/login/";
        return;
    }

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
            credentials: "include"
        });

        const data = await response.json();

        if (response.ok && data.success) {
            alert("Appointment booked successfully!");
            closeModal();
        } else {
            alert("Error: " + (data.error || "Something went wrong."));
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
    }
});


// ==============================
// Helper: Get CSRF Token
// ==============================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
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
document.addEventListener("DOMContentLoaded", async () => {
    await checkLoginStatus(); // ✅ Ensure login status before rendering buttons
    loadDoctors();
});
