function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

fetch("/send-message/", {
    method: "POST",
    headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        subject: "Test",
        body: "This is a test"
    })
});
