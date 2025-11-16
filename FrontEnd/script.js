document.getElementById('form_user').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const jsonData = {};

    for (let [key, value] of formData.entries()) {
        jsonData[key] = value;
    }

    fetch('/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('short:', data);

        const answerElement = document.getElementById('answer');
        const container = document.getElementById('answer-container');

        answerElement.textContent = data.short_key;
        container.style.display = 'block';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while sending data');
    })
});