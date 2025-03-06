document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const numQuestionsSlider = document.getElementById('numQuestions');
    const questionValue = document.getElementById('questionValue');
    const domainInput = document.getElementById('domain');
    const domainOptions = document.getElementById('domainOptions');
    const difficultyBtns = document.querySelectorAll('.difficulty-btn');
    const dialHand = document.getElementById('dialHand');
    const timerValue = document.getElementById('timerValue');
    const fileUpload = document.getElementById('fileUpload');
    const pdfFile = document.getElementById('pdfFile');
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    const configForm = document.getElementById('configForm');
    const domainError = document.getElementById('domainError');
    const fileError = document.getElementById('fileError');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const progressBar = document.getElementById('progressBar');
    const loadingText = document.getElementById('loadingText');
    const dialMarkers = document.getElementById('dialMarkers');
    
    // Initialize values
    let selectedDifficulty = 'medium';
    let timerMinutes = 10;
    let hasFile = false;
    
    // Create dial markers
    for (let i = 0; i < 12; i++) {
      const marker = document.createElement('div');
      marker.className = 'dial-marker';
      marker.style.transform = `rotate(${i * 30}deg) translateX(-50%)`;
      dialMarkers.appendChild(marker);
    }
    
    // Number of Questions Slider
    numQuestionsSlider.addEventListener('input', function() {
      questionValue.textContent = this.value;
      
      // Add pulse animation
      questionValue.style.animation = 'none';
      setTimeout(() => {
        questionValue.style.animation = 'pulse 0.5s';
      }, 10);
    });
    
    // Domain Dropdown
    domainInput.addEventListener('click', function() {
      domainOptions.classList.toggle('show');
    });
    
    document.querySelectorAll('.dropdown-option').forEach(option => {
      option.addEventListener('click', function() {
        const value = this.getAttribute('data-value');
        domainInput.value = this.textContent;
        domainInput.setAttribute('data-value', value);
        domainOptions.classList.remove('show');
        
        // Validation: If domain selected, clear file
        if (hasFile) {
          clearFileInput();
        }
        
        domainError.classList.remove('show');
      });
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
      if (!e.target.closest('.dropdown')) {
        domainOptions.classList.remove('show');
      }
    });
    
    // Difficulty Buttons
    difficultyBtns.forEach(btn => {
      if (btn.getAttribute('data-difficulty') === 'medium') {
        btn.classList.add('active');
      }
      
      btn.addEventListener('click', function() {
        difficultyBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        selectedDifficulty = this.getAttribute('data-difficulty');
      });
    });
    
    // Timer Dial
    let isDragging = false;
    const minTimer = 5;
    const maxTimer = 60;
    
    function updateDialPosition(e) {
      if (!isDragging) return;
      
      const dial = document.querySelector('.dial');
      const rect = dial.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      
      const angle = Math.atan2(e.clientY - centerY, e.clientX - centerX);
      const degrees = angle * (180 / Math.PI) + 90;
      
      // Normalize to 0-360
      let normalizedDegrees = degrees < 0 ? degrees + 360 : degrees;
      
      // Map 0-360 degrees to minTimer-maxTimer minutes
      const percentage = normalizedDegrees / 360;
      timerMinutes = Math.floor(minTimer + percentage * (maxTimer - minTimer));
      
      // Update dial position
      dialHand.style.transform = `translateX(-50%) rotate(${normalizedDegrees}deg)`;
      timerValue.textContent = timerMinutes;
    }
    
    document.querySelector('.dial').addEventListener('mousedown', function(e) {
      isDragging = true;
      updateDialPosition(e);
    });
    
    document.addEventListener('mousemove', updateDialPosition);
    document.addEventListener('mouseup', function() {
      isDragging = false;
    });
    
    // File Upload
    fileUpload.addEventListener('click', function() {
      pdfFile.click();
    });
    
    pdfFile.addEventListener('change', function() {
      if (this.files.length > 0) {
        hasFile = true;
        fileName.textContent = this.files[0].name;
        filePreview.style.display = 'block';
        
        // Validation: If file selected, clear domain
        if (domainInput.getAttribute('data-value')) {
          domainInput.value = '';
          domainInput.setAttribute('data-value', '');
        }
        
        fileError.classList.remove('show');
      }
    });
    
    // Drag and Drop
    fileUpload.addEventListener('dragover', function(e) {
      e.preventDefault();
      this.classList.add('drag-over');
    });
    
    fileUpload.addEventListener('dragleave', function() {
      this.classList.remove('drag-over');
    });
    
    fileUpload.addEventListener('drop', function(e) {
      e.preventDefault();
      this.classList.remove('drag-over');
      
      if (e.dataTransfer.files.length > 0 && e.dataTransfer.files[0].type === 'application/pdf') {
        pdfFile.files = e.dataTransfer.files;
        hasFile = true;
        fileName.textContent = e.dataTransfer.files[0].name;
        filePreview.style.display = 'block';
        
        // Validation: If file selected, clear domain
        if (domainInput.getAttribute('data-value')) {
          domainInput.value = '';
          domainInput.setAttribute('data-value', '');
        }
        
        fileError.classList.remove('show');
      }
    });
    
    function clearFileInput() {
      pdfFile.value = '';
      filePreview.style.display = 'none';
      hasFile = false;
    }
    
    // Form Submission
    configForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      setInterval(() => {
        //loadingOverlay.classList.remove('show');
        // Here you would typically redirect or show results
        fetch('http://127.0.0.1:3000/checkmcqdone', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
           /* numQuestions: numQuestionsSlider.value,
            domain: domainInput.getAttribute('data-value'),
            difficulty: selectedDifficulty,
            timer: timerMinutes,
            hasFile*/
          })
        }).then(
          response => response.json()
        ).then(data => {
          console.log(data);
          if(data.status == "done")
          {
            alert('Questions already generated!');
            window.location.href = "http://127.0.0.1:3000/showmcq";
          }
        });
      }, 5000);

      // Validation
      let isValid = true;
      
      // Check if either domain or file is selected
      if (!domainInput.getAttribute('data-value') && !hasFile) {
        domainError.classList.add('show');
        fileError.classList.add('show');
        isValid = false;
      } else {
        domainError.classList.remove('show');
        fileError.classList.remove('show');
      }
      
      if (isValid) {
        // Show loading animation
        loadingOverlay.classList.add('show');
        
        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
          progress += Math.random() * 5;
          if (progress >= 100) {
            progress = 0;
            //clearInterval(interval);
            
            // Simulate completion after full progress
           
          }
          
          progressBar.style.width = `${progress}%`;
          
          // Update loading text based on progress
          if (progress < 30) {
            loadingText.textContent = 'Analyzing content...';
          } else if (progress < 60) {
            loadingText.textContent = 'Generating questions...';
          } else if (progress < 90) {
            loadingText.textContent = 'Finalizing...';
          } else {
            loadingText.textContent = 'Almost done!';
          }
        }, 100);
      }
    });
  });
