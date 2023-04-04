document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('tr.patient_row').forEach((row) => {
        row.addEventListener('mouseover', highlightRow);
        row.addEventListener('mouseleave', highlightRow);
    })

    document.querySelectorAll('ul#sort li').forEach((item) => {
        item.addEventListener('click', setSortMethod);
    })

    try {
        highlightSortMethod();
    } catch {
        console.log('Not performing GET request because no user is present.');
    }
});

function highlightRow(e) {
    // Event.target references the single element that the event happened to: https://developer.mozilla.org/en-US/docs/Web/API/Event/target
    // Event.currentTarget references the element(s) whose event handler(s) responded to the event as it bubbles up the DOM: https://developer.mozilla.org/en-US/docs/Web/API/Event/currentTarget
    // I only attached event listeners to the TR elements so their event handlers are the ones that respond to the event, so Event.currentTarget gets me a TR element here
    const row = e.currentTarget;
    if (e.type === 'mouseover') {
        row.style.backgroundColor = 'lightgreen';
    } else if (e.type === 'mouseleave') {
        row.style.backgroundColor = 'lightblue';
    }
}

function setSortMethod(e) {
    const csrftoken = getCookie('csrftoken');
    const sortMethod = e.target.innerHTML;

    // AJAX call to API
    // Source: https://docs.djangoproject.com/en/4.1/howto/csrf/#setting-the-token-on-the-ajax-request
    fetch('/sort', {
        method: 'PUT',
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        body: JSON.stringify({sortMethod: sortMethod}) // stringify() converst JS object to JSON format
    })
    .then(response => {
        if (response.status != 302) {
            console.log('Problem with PUT request. Status not 302.');
        }
        else {
            location.reload(); // Reload page
        }
    })
}

function highlightSortMethod() {
    // AJAX call to API
    fetch('/preference')
    .then(response => response.json()) // Despite the name, json() parses the JSON response into JS object: https://developer.mozilla.org/en-US/docs/Web/API/Response/json
    .then((data) => {
        // Get user's sort preference
        preference = data["sortPreference"];

        // API returns null if user isn't a doctor
        if (preference === null) {return;}

        // Highlight the option to reflect this
        let sortOption;
        document.querySelectorAll('ul#sort *').forEach((option) => {
            if (option.innerHTML === preference) {
                sortOption = option;
            }
        })
        sortOption.style.backgroundColor = 'cyan';
    })
    .catch((error) => {
        console.log("Error:", error);
    })
}

// Source: https://docs.djangoproject.com/en/4.1/howto/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

