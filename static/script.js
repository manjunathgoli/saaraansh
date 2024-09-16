// Event listener for each media card
document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', function () {
        const mediaType = this.getAttribute('data-media-type');
        document.getElementById('prompt-input').setAttribute('data-media-type', mediaType);

        if (mediaType === 'text') {
            document.getElementById('prompt-input').style.display = 'block';
            document.getElementById('text-input-section').style.display = 'block';
            document.getElementById('cards-section').style.display = 'none';
            document.getElementById('loading-section').style.display = 'none';
        } else {
            document.getElementById('file-input').click();
            document.getElementById('cards-section').style.display = 'none';
            document.getElementById('loading-section').style.display = 'block';
        }
    });
});

// Event listener for file input change (non-text media types)
document.getElementById('file-input').addEventListener('change', () => {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    const mediaType = document.getElementById('prompt-input').getAttribute('data-media-type');
    
    if (file) {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('media_type', mediaType);

        const inputContent = document.getElementById('input-content');
        inputContent.innerHTML = "";

        if (mediaType === 'image') {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.alt = 'Selected Image';
            img.style.maxWidth = '100%';
            inputContent.appendChild(img);
        } else if (mediaType === 'audio') {
            const audio = document.createElement('audio');
            audio.controls = true;
            audio.src = URL.createObjectURL(file);
            inputContent.appendChild(audio);
        } else if (mediaType === 'video') {
            const video = document.createElement('video');
            video.controls = true;
            video.style.maxWidth = '100%';
            video.src = URL.createObjectURL(file);
            inputContent.appendChild(video);
        }

        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
        .then(summary => {
            document.getElementById('loading-section').style.display = 'none';
            document.getElementById('output-section').style.display = 'flex';
            document.getElementById('summary-content').textContent = summary;
        });
    } else {
        alert("No file selected!");
    }
});

// Event listener for send button (text summarization)
document.getElementById('summary-icon').addEventListener('click', () => {
    const inputField = document.getElementById('prompts-input');
    const mediaType = inputField.getAttribute('data-media-type');
    const inputValue = inputField.value;

    if (mediaType === 'text' && inputValue.trim() !== "") {
        const formData = new FormData();
        formData.append('media_type', mediaType);
        formData.append('input_text', inputValue);

        document.getElementById('text-input-section').style.display = 'none';
        document.getElementById('loading-section').style.display = 'block';

        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
        .then(summary => {
            document.getElementById('loading-section').style.display = 'none';
            document.getElementById('output-section').style.display = 'flex';
            document.getElementById('input-content').textContent = inputValue;
            document.getElementById('summary-content').textContent = summary;

            // Display the slider
            document.querySelector('.slider-container').style.display = 'block';
        });
    } else {
        alert("Please enter text for summarization!");
    }
});

// Event listener for the summary length slider
document.getElementById('summary-length-slider').addEventListener('input', () => {
    const sliderValue = document.getElementById('summary-length-slider').value;
    const mediaType = document.getElementById('prompt-input').getAttribute('data-media-type');
    const inputValue = document.getElementById('input-content').textContent;

    if (mediaType === 'text' && inputValue.trim() !== "") {
        console.log("Slider value:", sliderValue); // Check slider value
        const formData = new FormData();
        formData.append('media_type', mediaType);
        formData.append('input_text', inputValue);
        formData.append('summary_length', sliderValue);

        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
        .then(updatedSummary => {
            console.log("Updated summary:", updatedSummary); // Check response from server
            document.getElementById('summary-content').textContent = updatedSummary;
        }).catch(error => {
            console.error("Error fetching updated summary:", error); // Handle errors
        });
    }
});

// Updated event listener for the send button (text summarization)
document.getElementById('send-icon').addEventListener('click', () => {
    const inputField = document.getElementById('prompt-input');  // For prompt input
    const mediaType = inputField.getAttribute('data-media-type');
    const promptValue = inputField.value;
    const inputText = document.getElementById('prompt-input').value;  // This should be used  // For main input text to summarize (assuming this exists)

    console.log("Media Type:", mediaType);  // Debugging: Check media type
    console.log("Prompt Value:", promptValue);  // Debugging: Check prompt value
    console.log("Input Text:", inputText);  // Debugging: Check if input text is captured

    // Check if prompt and inputText are filled
    if (mediaType === 'text' && promptValue.trim() !== "" && inputText.trim() !== "") {
        const formData = new FormData();
        formData.append('media_type', mediaType);
        formData.append('prompt', promptValue);
        formData.append('input_text', inputText);  // Add input_text to form data

        document.getElementById('loading-section').style.display = 'block';  // Show loading spinner

        fetch('/generate-response', {
            method: 'POST',
            body: formData
        }).then(response => response.json())
        .then(data => {
            console.log("Response Data:", data);  // Debugging: Check response data
            document.getElementById('loading-section').style.display = 'none';  // Hide loading spinner
            document.getElementById('output-section').style.display = 'flex';  // Show summary output
            document.getElementById('summary-content').innerHTML = data.summary;  // Display the summary
        }).catch(error => {
            console.error("Error fetching summary:", error);  // Handle errors
        });
    } else {
        alert("Please enter both prompt and text for summarization!");
    }
});
