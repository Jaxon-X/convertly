// DOM elementlarini tanlab olish
const dropZone = document.querySelector('.drop-zone');
const fileInput = document.getElementById('fileInput');
const filePreview = document.querySelector('.file-preview');
const fileName = document.querySelector('.file-name');
const removeFileBtn = document.querySelector('.remove-file');
const convertBtn = document.querySelector('.convert-button');
const conversionProgress = document.querySelector('.conversion-progress');
const downloadSection = document.querySelector('.download-section');
const downloadButton = document.querySelector('.download-button');
const convertAnotherBtn = document.querySelector('.convert-another');
const resultFilename = document.querySelector('.result-filename');

// Faylni drag & drop qilish
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
   const validTypes = ['.png', '.jpeg'];
   const fileExtension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
   if (!validTypes.includes(fileExtension)) {
       alert('Faqat .png yoki .jpeg formatdagi fayllar qabul qilinadi');
       return false;
   }
   if (file.size > 50 * 1024 * 1024) { // 50MB
       alert('Fayl hajmi 50MB dan oshmasligi kerak');
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

// Faylni konvertatsiya qilish
convertBtn.addEventListener('click', async () => {
   const file = fileInput.files[0];
   if (!file) return;

   const formData = new FormData();
   formData.append('file', file);

   filePreview.style.display = 'none';
   conversionProgress.style.display = 'block';

   try {
       // Konvertatsiya API ga yuborish
       const response = await fetch('http://127.0.0.1:8000/api/convert/image-to-pdf/', {
           method: 'POST',
           body: formData
       });

       const data = await response.json();

       if (!response.ok) {
           throw new Error(data.error || 'Konvertatsiya jarayonida xatolik yuz berdi');
       }

       // Task statusini tekshirish
       const taskId = data.task_id;
       const checkStatus = async () => {
           const statusResponse = await fetch(`http://127.0.0.1:8000/api/convert/status/${taskId}/`);
           const statusData = await statusResponse.json();
           console.log(statusData)

           if (statusData.task_status === 'SUCCESS') {
               showDownloadSection(data.filename);
               clearInterval(statusInterval);
           } else if (statusData.task_status === 'FAILURE') {
               clearInterval(statusInterval);
               throw new Error('Konvertatsiya muvaffaqiyatsiz yakunlandi');
           }
       };

       // Har 2 soniyada status tekshirish
       const statusInterval = setInterval(checkStatus, 2000);
       // Birinchi tekshiruv
       await checkStatus();

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
       a.download = filename;
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
}