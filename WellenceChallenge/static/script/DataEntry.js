// Set the minimum date and time to the current time
function setMinDateTime() {
    var now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    var isoString = now.toISOString().slice(0, 16);
    document.getElementById("due_by").setAttribute("min", isoString);
}

// When the page loads, set the minimum date and time
window.onload = setMinDateTime;

// When the form is submitted, prevent the default behavior and submit the data
document.getElementById('taskForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const jsonData = Object.fromEntries(formData);

    jsonData.priority = parseInt(jsonData.priority);
    jsonData.is_urgent = formData.has('is_urgent');

    console.log('Submitting data:', JSON.stringify(jsonData, null, 2));

    try {
        const response = await fetch('/api/tasks/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify(jsonData)
        });

        const responseData = await response.json();
        console.log('Server response:', response.status, responseData);

        if (response.ok) {
            alert('Task added successfully. ID: ' + responseData.id);
            this.reset();
        } else {
            alert('Error adding task: ' + JSON.stringify(responseData));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error: ' + error.message);
    }
});