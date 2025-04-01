/**
 * Validates if a radio button is selected before form submission.
 * Displays an alert if no radio button is selected.
 * @returns {boolean} - Returns true if a radio button is selected, false otherwise.
 */
function validateSelection() {
    // Get all radio buttons with the name "dataset"
    const radios = document.querySelectorAll('input[name="dataset"]');
    let isSelected = false;

    // Check if any radio button is selected
    for (const radio of radios) {
        if (radio.checked) {
            isSelected = true;
            break;
        }
    }

    // If no radio button is selected, show an alert and prevent form submission
    if (!isSelected) {
        alert("Please select an analysis type before proceeding.");
        return false; // Prevent form submission
    }

    return true; // Allow form submission
}

/**
 * Toggles the visibility of the download and upload buttons
 * based on the selected radio button.
 */
function toggleButtons() {
    // Get all radio buttons with the name "dataset"
    const radios = document.querySelectorAll('input[name="dataset"]');
    let isSelected = false;

    // Check if any radio button is selected
    for (const radio of radios) {
        if (radio.checked) {
            isSelected = true;
            break;
        }
    }

    // Get the download and upload forms
    const downloadForm = document.getElementById('download-form');
    const uploadForm = document.getElementById('upload-form');

    // Show or hide the forms based on the selection
    if (isSelected) {
        downloadForm.style.display = 'block';
        uploadForm.style.display = 'block';
    } else {
        downloadForm.style.display = 'none';
        uploadForm.style.display = 'none';
    }
}