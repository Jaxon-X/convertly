// DOM elementlarini tanlab olish
const dropZone = document.querySelector('.drop-zone');
const fileInput = document.getElementById('fileInput');
const filePreview = document.querySelector('.file-preview');
const fileName = document.querySelector('.file-name');
const removeFileBtn = document.querySelector('.remove-file');
const convertBtn = document.querySelector('.convert-button');
const conversionProgress = document.querySelector('.conversion-progress');
const progressCircle = document.querySelector('.progress-ring-circle');
const progressPercent = document.querySelector('.progress-percent');
const downloadSection = document.querySelector('.download-section');
const downloadButton = document.querySelector('.download-button');
const convertAnotherBtn = document.querySelector('.convert-another');
const resultFilename = document.querySelector('.result-filename');

// Progress ring animation uchun o'zgaruvchilar
const radius = 52;
const circumference = radius * 2 * Math.PI;
progressCircle.style.strokeDasharray = `${circumference} ${circumference}`;
progressCircle.style.strokeDashoffset = circumference;

// Faylni drag & drop qilish
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drop-zone-active');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drop-zone-active');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drop-zone-active');
    const file = e.dataTransfer.files[0];
    if (file && isValidFile(file)) {
        handleFileSelect(file);
    }
});

// File input orqali fayl tanlash
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file && isValidFile(file)) {
        handleFileSelect(file);
    }
});

// Faylni tekshirish
function isValidFile(file) {
    const validTypes = ['.odt'];
    const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    if (!validTypes.includes(fileExtension)) {
        alert('Faqat .odt formatdagi fayllar qabul qilinadi');
        return false;
    }
    if (file.size > 50 * 1024 * 1024) { // 10MB
        alert('Fayl hajmi 10MB dan oshmasligi kerak');
        return false;
    }
    return true;
}

// Faylni tanlangandan keyin ko'rsatish
function handleFileSelect(file) {
    dropZone.style.display = 'none';
    filePreview.style.display = 'block';
    fileName.textContent = file.name;
    fileInput.files = new DataTransfer().files;
    const newFileList = new DataTransfer();
    newFileList.items.add(file);
    fileInput.files = newFileList.files;
}

// Tanlangan faylni o'chirish
removeFileBtn.addEventListener('click', () => {
    fileInput.value = '';
    dropZone.style.display = 'block';
    filePreview.style.display = 'none';
});

// Konvertatsiya progressini yangilash
function setProgress(percent) {
    const offset = circumference - (percent / 100) * circumference;
    progressCircle.style.strokeDashoffset = offset;
    progressPercent.textContent = `${percent}%`;
}

// Faylni konvertatsiya qilish
convertBtn.addEventListener('click', async () => {
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    filePreview.style.display = 'none';
    conversionProgress.style.display = 'flex';

    try {
        // Konvertatsiya API ga yuborish
        const response = await fetch(' http://127.0.0.1:8000/api/convert/odt-to-pdf/', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Konvertatsiya jarayonida xatolik yuz berdi');
        }

        // Progress animatsiyasi (simulate)
        let progress = 0;
        const interval = setInterval(() => {
            progress += 2;
            setProgress(progress);
            if (progress >= 100) {
                clearInterval(interval);
                showDownloadSection(data.filename);
            }
        }, 50);

    } catch (error) {
        console.error('Error:', error);
        alert('Xatolik yuz berdi: ' + error.message);
        resetConverter();
    }
});

// Yuklash bo'limini ko'rsatish
function showDownloadSection(filename) {
    conversionProgress.style.display = 'none';
    downloadSection.style.display = 'flex';
    resultFilename.textContent = filename;
}

// PDF ni yuklab olish
downloadButton.addEventListener('click', async () => {
    const filename = resultFilename.textContent;
    if (!filename) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/convert/download/${filename}/`);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Yuklashda xatolik yuz berdi');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename; // Fayl nomi APIdan kelgan nomdan foydalaniladi
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    } catch (error) {
        console.error('Error:', error);
        alert('Faylni yuklashda xatolik yuz berdi: ' + error.message);
    }
});

// Yangi fayl konvertatsiya qilish
convertAnotherBtn.addEventListener('click', resetConverter);

// Konverter holatini boshlang'ich holatga qaytarish
function resetConverter() {
    fileInput.value = '';
    dropZone.style.display = 'block';
    filePreview.style.display = 'none';
    conversionProgress.style.display = 'none';
    downloadSection.style.display = 'none';
    setProgress(0);
}