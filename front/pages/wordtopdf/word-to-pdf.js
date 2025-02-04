document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.querySelector('.drop-zone');
    const fileInput = document.querySelector('.file-input');
    const filePreview = document.querySelector('.file-preview');
    const conversionProgress = document.querySelector('.conversion-progress');
    const downloadSection = document.querySelector('.download-section');
    const progressRing = document.querySelector('.progress-ring-circle');
    const progressPercent = document.querySelector('.progress-percent');
    const selectButton = document.querySelector('.select-button'); // Select button element

    const circumference = progressRing.getTotalLength();
    progressRing.style.strokeDasharray = `${circumference} ${circumference}`;

    function setProgress(percent) {
        const offset = circumference - (percent / 100 * circumference);
        progressRing.style.strokeDashoffset = offset;
        progressPercent.textContent = `${Math.round(percent)}%`;
    }

    function showFilePreview(file) {
        document.querySelector('.file-name').textContent = file.name;
        dropZone.style.display = 'none';
        filePreview.style.display = 'block';
    }

    function startConversion() {
        filePreview.style.display = 'none';
        conversionProgress.style.display = 'block';
        setProgress(0);

        const interval = setInterval(() => {
            const currentProgress = parseInt(progressPercent.textContent);
            if (currentProgress < 90) {
                setProgress(currentProgress + 10);
            }
        }, 500);

        return interval;
    }

    function handleFile(file) {
        if (!file) return;
        showFilePreview(file);

        document.querySelector('.convert-button').onclick = () => {
            const progressInterval = startConversion();
            const formData = new FormData();
            formData.append('file', file);

            fetch('/api/doc-to-pdf/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                clearInterval(progressInterval);
                setProgress(100);

                setTimeout(() => {
                    conversionProgress.style.display = 'none';
                    downloadSection.style.display = 'block';
                    document.querySelector('.result-filename').textContent = data.filename;

                    document.querySelector('.download-button').onclick = () => {
                        downloadFile(data.filename);
                    };
                }, 500);
            })
            .catch(error => {
                clearInterval(progressInterval);
                alert('An error occurred during conversion: ' + error.message);
            });
        };
    }

    // Event listeners
    document.querySelector('.convert-another').onclick = () => {
        location.reload();
    };

    document.querySelector('.remove-file').onclick = () => {
        dropZone.style.display = 'block';
        filePreview.style.display = 'none';
        fileInput.value = '';
    };

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        handleFile(e.dataTransfer.files[0]);
    });

    fileInput.addEventListener('change', (e) => {
        handleFile(e.target.files[0]);
    });

    // Add event listener to select button to trigger file input click
    selectButton.addEventListener('click', () => {
        // Open the file input dialog
        document.getElementById('fileInput').click();
    });
});

function downloadFile(filename) {
    window.location.href = `/api/download/${filename}`;
}
