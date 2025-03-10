document.addEventListener('DOMContentLoaded', () => {
  // Slider Update
  const slider = document.getElementById('numQuestions');
  const sliderValue = document.getElementById('questionValue');
  slider.addEventListener('input', (e) => {
    sliderValue.textContent = e.target.value;
  });

  // Domain Selection
  const domainOptions = document.querySelectorAll('.dropdown-option');
  const domainInput = document.getElementById('domain');
  domainOptions.forEach(option => {
    option.addEventListener('click', () => {
      domainInput.dataset.value = option.dataset.value;
      domainInput.value = option.textContent;
      document.getElementById('domainError').style.display = 'none';
    });
  });

  // Difficulty Selection
  document.querySelectorAll('.difficulty-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.difficulty-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  // File Upload Handling
  const fileUpload = document.getElementById('fileUpload');
  const pdfInput = document.getElementById('pdfFile');
  const fileName = document.getElementById('fileName');
  
  fileUpload.addEventListener('click', () => pdfInput.click());
  pdfInput.addEventListener('change', handleFileSelect);

  function handleFileSelect(e) {
    const file = e.target.files[0];
    if (!validatePDF(file)) return;
    
    fileName.textContent = file.name;
    document.getElementById('filePreview').style.display = 'block';
    document.getElementById('fileError').style.display = 'none';
  }

  // Drag & Drop Handling
  fileUpload.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUpload.classList.add('dragover');
  });

  fileUpload.addEventListener('dragleave', () => {
    fileUpload.classList.remove('dragover');
  });

  fileUpload.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUpload.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (validatePDF(file)) {
      pdfInput.files = e.dataTransfer.files;
      handleFileSelect({ target: pdfInput });
    }
  });

  // Form Submission
  document.getElementById('configForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    const formData = new FormData();
    formData.append('num_questions', slider.value);
    formData.append('domain', domainInput.dataset.value);
    formData.append('difficulty', document.querySelector('.difficulty-btn.active').dataset.difficulty);
    formData.append('time', `${document.getElementById('minutes').value}:${document.getElementById('seconds').value}`);
    if (pdfInput.files[0]) formData.append('pdf', pdfInput.files[0]);

    try {
      showLoading();
      const response = await fetch('/generate_questions', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      
      if (response.ok) {
        window.location.href = `/quiz?data=${encodeURIComponent(JSON.stringify(data.questions))}`;
      } else {
        showError(data.error || 'Failed to generate questions');
      }
    } catch (error) {
      showError('Network error. Please check your connection.');
    } finally {
      hideLoading();
    }
  });

  // Validation Functions
  function validatePDF(file) {
    if (!file) return false;
    
    const maxSize = parseInt(pdfInput.dataset.maxSize) || 5242880;
    if (file.size > maxSize) {
      showError('File size exceeds 5MB limit', 'fileError');
      pdfInput.value = '';
      return false;
    }
    if (file.type !== 'application/pdf') {
      showError('Only PDF files are allowed', 'fileError');
      pdfInput.value = '';
      return false;
    }
    return true;
  }

  function validateForm() {
    let isValid = true;
    const domain = domainInput.dataset.value;
    const pdfFile = pdfInput.files[0];

    if (!domain && !pdfFile) {
      showError('Please select a domain or upload a PDF', 'domainError');
      isValid = false;
    }
    
    return isValid;
  }

  function showError(message, elementId) {
    const errorElement = document.getElementById(elementId);
    errorElement.textContent = message;
    errorElement.style.display = 'block';
    setTimeout(() => errorElement.style.display = 'none', 5000);
  }

  // Loading Animation
  function showLoading() {
    const overlay = document.getElementById('loadingOverlay');
    overlay.style.display = 'flex';
    simulateProgress();
  }

  function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
  }

  function simulateProgress() {
    let width = 0;
    const progressBar = document.getElementById('progressBar');
    const interval = setInterval(() => {
      if (width >= 90) {
        clearInterval(interval);
        return;
      }
      width++;
      progressBar.style.width = `${width}%`;
    }, 100);
  }
});
