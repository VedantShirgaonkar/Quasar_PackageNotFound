// Sample quiz data for demonstration
const quizData = {
    accuracy: 75,
    totalQuestions: 20,
    correctAnswers: 15,
    incorrectAnswers: 5,
    timeTaken: "12:45",
    domainPerformance: [
        { domain: "Network Security", score: 85, questions: 5 },
        { domain: "Application Security", score: 70, questions: 5 },
        { domain: "Cloud Security", score: 60, questions: 5 },
        { domain: "Cryptography", score: 80, questions: 5 }
    ],
    questions: [
        {
            id: 1,
            domain: "Network Security",
            question: "Which of the following is NOT a common network security threat?",
            options: [
                { label: "A", text: "Man-in-the-Middle Attack" },
                { label: "B", text: "DDoS Attack" },
                { label: "C", text: "SQL Injection" },
                { label: "D", text: "ARP Poisoning" }
            ],
            correctAnswer: "C",
            userAnswer: "C",
            explanation: "SQL Injection is primarily an application security threat that targets databases, not a network security threat."
        },
        {
            id: 2,
            domain: "Application Security",
            question: "What is the main purpose of input validation in web applications?",
            options: [
                { label: "A", text: "To improve user experience" },
                { label: "B", text: "To prevent malicious input that could lead to attacks" },
                { label: "C", text: "To reduce server load" },
                { label: "D", text: "To collect user analytics" }
            ],
            correctAnswer: "B",
            userAnswer: "A",
            explanation: "Input validation is primarily a security measure to prevent attacks like SQL injection, XSS, and command injection by ensuring that only properly formatted data enters the application."
        },
        {
            id: 3,
            domain: "Cloud Security",
            question: "Which security principle refers to granting users only the permissions they need to perform their job?",
            options: [
                { label: "A", text: "Defense in Depth" },
                { label: "B", text: "Least Privilege" },
                { label: "C", text: "Zero Trust" },
                { label: "D", text: "Segregation of Duties" }
            ],
            correctAnswer: "B",
            userAnswer: "B",
            explanation: "The Principle of Least Privilege (PoLP) states that users should be given only the minimum levels of access necessary to complete their job functions."
        },
        {
            id: 4,
            domain: "Cryptography",
            question: "Which of the following is an asymmetric encryption algorithm?",
            options: [
                { label: "A", text: "AES" },
                { label: "B", text: "DES" },
                { label: "C", text: "RSA" },
                { label: "D", text: "Blowfish" }
            ],
            correctAnswer: "C",
            userAnswer: "C",
            explanation: "RSA is an asymmetric (public key) encryption algorithm. AES, DES, and Blowfish are all symmetric encryption algorithms."
        },
        {
            id: 5,
            domain: "Network Security",
            question: "What type of attack attempts to exhaust system resources to make them unavailable?",
            options: [
                { label: "A", text: "Phishing" },
                { label: "B", text: "Ransomware" },
                { label: "C", text: "DoS/DDoS" },
                { label: "D", text: "Social Engineering" }
            ],
            correctAnswer: "C",
            userAnswer: "C",
            explanation: "Denial of Service (DoS) and Distributed Denial of Service (DDoS) attacks aim to make resources unavailable by overwhelming them with traffic or requests."
        }
    ]
};

// DOM Elements
const loadingScreen = document.getElementById('loading-screen');
const resultsDashboard = document.getElementById('results-dashboard');
const progressBar = document.getElementById('progress-bar');
const loadingPercentage = document.querySelector('.loading-percentage');
const accuracyCircle = document.getElementById('accuracy-circle');
const accuracyPercentage = document.getElementById('accuracy-percentage');
const accuracyMessage = document.getElementById('accuracy-message');
const totalQuestionsEl = document.getElementById('total-questions');
const correctAnswersEl = document.getElementById('correct-answers');
const incorrectAnswersEl = document.getElementById('incorrect-answers');
const timeTakenEl = document.getElementById('time-taken');
const questionsList = document.getElementById('questions-list');
const domainChart = document.getElementById('domain-chart');
const domainTooltip = document.getElementById('domain-tooltip');
const domainLegend = document.getElementById('domain-legend');
const leaderboardBtn = document.getElementById('leaderboard-btn');
const leaderboardModal = document.getElementById('leaderboard-modal');
const closeModal = document.querySelector('.close-modal');
const replayBtn = document.getElementById('replay-btn');
const yourLeaderboardScore = document.getElementById('your-leaderboard-score');
const particlesContainer = document.getElementById('particles-container');

// Colors for domain chart (cyberpunk theme)
const chartColors = [
    '#6C56FC', // Primary
    '#FC56C4', // Secondary
    '#56FCB1', // Accent
    '#FCBE56', // Warning
    '#5689FC', // Blue variant
    '#FC5656'  // Red variant
];

// Initialize loading animation
function initLoading() {
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 5;
        if (progress > 100) {
            progress = 100;
            clearInterval(interval);
            setTimeout(() => {
                loadingScreen.classList.add('hidden');
                resultsDashboard.classList.remove('hidden');
                initResults();
            }, 500);
        }
        progressBar.style.width = `${progress}%`;
        loadingPercentage.textContent = `${Math.floor(progress)}%`;
    }, 100);
}

// Initialize results dashboard
function initResults() {
    updateAccuracyDisplay();
    updateStats();
    renderQuestionsList();
    renderDomainChart();
    
    // Trigger confetti effect if accuracy is high
    if (quizData.accuracy >= 70) {
        createConfetti();
    }
}

// Update accuracy display with animation
function updateAccuracyDisplay() {
    let currentPercentage = 0;
    const targetPercentage = quizData.accuracy;
    
    // Determine color based on accuracy
    let glowColor;
    if (targetPercentage >= 80) {
        glowColor = 'rgba(86, 252, 177, 0.7)'; // Green glow
        accuracyMessage.textContent = 'EXCELLENT PERFORMANCE!';
    } else if (targetPercentage >= 50) {
        glowColor = 'rgba(252, 190, 86, 0.7)'; // Yellow-orange glow
        accuracyMessage.textContent = 'GOOD EFFORT!';
    } else {
        glowColor = 'rgba(252, 86, 86, 0.7)'; // Red glow
        accuracyMessage.textContent = 'NEEDS IMPROVEMENT';
    }
    
    // Set glow color
    accuracyCircle.style.boxShadow = `0 0 30px ${glowColor}`;
    
    // Animate percentage counter
    const interval = setInterval(() => {
        if (currentPercentage < targetPercentage) {
            currentPercentage++;
            accuracyPercentage.textContent = `${currentPercentage}%`;
            
            // Apply pulsating animation at milestone percentages
            if (currentPercentage % 25 === 0) {
                accuracyCircle.classList.add('pulse');
                setTimeout(() => {
                    accuracyCircle.classList.remove('pulse');
                }, 500);
            }
        } else {
            clearInterval(interval);
        }
    }, 20);
}

// Update statistics with counter animations
function updateStats() {
    animateCounter(totalQuestionsEl, 0, quizData.totalQuestions, 1000);
    animateCounter(correctAnswersEl, 0, quizData.correctAnswers, 1000);
    animateCounter(incorrectAnswersEl, 0, quizData.incorrectAnswers, 1000);
    timeTakenEl.textContent = quizData.timeTaken;
}

// Animate number counter
function animateCounter(element, start, end, duration) {
    let current = start;
    const increment = (end - start) / (duration / 50);
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 50);
}

// Render questions list with animations
function renderQuestionsList() {
    questionsList.innerHTML = '';
    
    quizData.questions.forEach((question, index) => {
        const questionItem = document.createElement('div');
        questionItem.className = 'question-item';
        questionItem.classList.add(question.userAnswer === question.correctAnswer ? 'correct' : 'incorrect');
        
        // Add animation delay for each question
        questionItem.style.animationDelay = `${index * 0.1}s`;
        
        // Add glitch effect for incorrect answers
        if (question.userAnswer !== question.correctAnswer) {
            setTimeout(() => {
                questionItem.classList.add('glitch');
                setTimeout(() => {
                    questionItem.classList.remove('glitch');
                }, 300);
            }, 1000 + index * 100);
        }
        
        questionItem.innerHTML = `
            <div class="question-number">Question ${question.id} • ${question.domain}</div>
            <div class="question-text">${question.question}</div>
            <div class="options-list">
                ${question.options.map(option => `
                    <div class="option ${option.label === question.correctAnswer ? 'correct' : ''} 
                                        ${option.label === question.userAnswer && option.label !== question.correctAnswer ? 'incorrect' : ''}
                                        ${option.label === question.userAnswer ? 'selected' : ''}">
                        <div class="option-label">${option.label}</div>
                        <div class="option-text">${option.text}</div>
                    </div>
                `).join('')}
            </div>
            <div class="explanation">${question.explanation}</div>
        `;
        
        questionsList.appendChild(questionItem);
    });
    
    // Display questions with a staggered animation
    const items = document.querySelectorAll('.question-item');
    items.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, 500 + index * 100);
    });
}

// Render domain performance chart
function renderDomainChart() {
    const ctx = domainChart.getContext('2d');
    const centerX = domainChart.width / 2;
    const centerY = domainChart.height / 2;
    const radius = Math.min(centerX, centerY) * 0.8;
    
    // Clear canvas
    ctx.clearRect(0, 0, domainChart.width, domainChart.height);
    
    // Prepare data for the chart
    const total = quizData.domainPerformance.reduce((sum, domain) => sum + domain.score, 0);
    let startAngle = -Math.PI / 2;
    
    // Create legend items
    domainLegend.innerHTML = '';
    
    // Draw each segment with animation
    quizData.domainPerformance.forEach((domain, index) => {
        const portion = domain.score / 100;
        const endAngle = startAngle + (Math.PI * 2 * portion);
        const color = chartColors[index % chartColors.length];
        
        // Animate segments drawing
        setTimeout(() => {
            drawPieSegment(ctx, centerX, centerY, radius, startAngle, endAngle, color, domain);
        }, index * 300);
        
        // Add legend item
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item';
        legendItem.innerHTML = `
            <div class="legend-color" style="background-color: ${color}"></div>
            <div class="legend-label">${domain.domain}: ${domain.score}%</div>
        `;
        domainLegend.appendChild(legendItem);
        
        // Store segment data for hover interactions
        domain.angles = { start: startAngle, end: endAngle };
        domain.color = color;
        
        startAngle = endAngle;
    });
    
    // Setup hover interactions
    setupChartInteractions();
}

// Draw pie chart segment with animation
function drawPieSegment(ctx, centerX, centerY, radius, startAngle, endAngle, color, domainData) {
    // Draw segment background
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, startAngle, endAngle);
    ctx.closePath();
    
    // Fill with gradient
    const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
    gradient.addColorStop(0, 'rgba(255, 255, 255, 0.2)');
    gradient.addColorStop(0.8, color);
    gradient.addColorStop(1, color);
    
    ctx.fillStyle = gradient;
    ctx.fill();
    
    // Add stroke
    ctx.lineWidth = 2;
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
    ctx.stroke();
    
    // Add domain name at center of the segment
    const midAngle = startAngle + (endAngle - startAngle) / 2;
    const textRadius = radius * 0.7;
    const textX = centerX + Math.cos(midAngle) * textRadius;
    const textY = centerY + Math.sin(midAngle) * textRadius;
    
    // Only add text for larger segments
    if (endAngle - startAngle > 0.4) {
        ctx.save();
        ctx.translate(textX, textY);
        ctx.rotate(midAngle + Math.PI / 2);
        ctx.textAlign = 'center';
        ctx.fillStyle = 'white';
        ctx.font = 'bold 12px sans-serif';
        ctx.fillText(`${domainData.score}%`, 0, 0);
        ctx.restore();
    }
    
    // Add glow effect for high scores
    if (domainData.score >= 80) {
        ctx.save();
        ctx.globalAlpha = 0.5;
        ctx.shadowColor = color;
        ctx.shadowBlur = 15;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.closePath();
        ctx.stroke();
        ctx.restore();
    }
}

// Setup interactions for the chart
function setupChartInteractions() {
    domainChart.addEventListener('mousemove', (e) => {
        const rect = domainChart.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = domainChart.width / 2;
        const centerY = domainChart.height / 2;
        
        // Calculate angle from center to mouse position
        const angle = Math.atan2(y - centerY, x - centerX);
        const adjustedAngle = angle < -Math.PI / 2 ? angle + Math.PI * 2 : angle;
        
        // Find domain segment at angle
        const domain = quizData.domainPerformance.find(d => 
            adjustedAngle >= d.angles.start && adjustedAngle <= d.angles.end
        );
        
        if (domain) {
            // Show tooltip
            domainTooltip.classList.remove('hidden');
            domainTooltip.style.left = `${e.clientX - rect.left + 10}px`;
            domainTooltip.style.top = `${e.clientY - rect.top + 10}px`;
            
            document.getElementById('domain-name').textContent = domain.domain;
            document.getElementById('domain-score').textContent = `Score: ${domain.score}%`;
            document.getElementById('domain-questions').textContent = `Questions: ${domain.questions}`;
            
            // Highlight segment
            const ctx = domainChart.getContext('2d');
            renderDomainChart();
            
            ctx.globalAlpha = 0.3;
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, Math.min(centerX, centerY) * 0.9, domain.angles.start, domain.angles.end);
            ctx.closePath();
            ctx.fillStyle = 'white';
            ctx.fill();
            ctx.globalAlpha = 1;
        } else {
            // Hide tooltip
            domainTooltip.classList.add('hidden');
        }
    });
    
    domainChart.addEventListener('mouseleave', () => {
        domainTooltip.classList.add('hidden');
        renderDomainChart();
    });
}

// Create confetti particles effect
function createConfetti() {
    const colors = ['#6C56FC', '#FC56C4', '#56FCB1', '#FCBE56', '#5689FC'];
    
    for (let i = 0; i < 100; i++) {
        setTimeout(() => {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Random properties
            const size = Math.random() * 8 + 4;
            const color = colors[Math.floor(Math.random() * colors.length)];
            const left = Math.random() * 100;
            const duration = Math.random() * 3 + 3;
            const delay = Math.random() * 2;
            
            // Apply styles
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.backgroundColor = color;
            particle.style.left = `${left}%`;
            particle.style.top = '0';
            particle.style.boxShadow = `0 0 10px ${color}`;
            
            // Apply animation
            particle.style.animation = `fall ${duration}s ease-in ${delay}s forwards`;
            
            // Add to container and remove after animation
            particlesContainer.appendChild(particle);
            setTimeout(() => {
                particle.remove();
            }, (duration + delay) * 1000);
        }, i * 50);
    }
    
    // Create falling animation if it doesn't exist
    if (!document.querySelector('style#confetti-style')) {
        const style = document.createElement('style');
        style.id = 'confetti-style';
        style.innerHTML = `
            @keyframes fall {
                0% {
                    transform: translateY(-20px) rotate(0deg);
                    opacity: 0;
                }
                10% {
                    opacity: 1;
                }
                100% {
                    transform: translateY(${window.innerHeight}px) rotate(720deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

// Modal Interactions
leaderboardBtn.addEventListener('click', () => {
    leaderboardModal.classList.remove('hidden');
    yourLeaderboardScore.textContent = `${quizData.accuracy}%`;
});

closeModal.addEventListener('click', () => {
    leaderboardModal.classList.add('hidden');
});

// Close modal when clicking outside content
leaderboardModal.addEventListener('click', (e) => {
    if (e.target === leaderboardModal) {
        leaderboardModal.classList.add('hidden');
    }
});

// Replay button
replayBtn.addEventListener('click', () => {
    // Simulate reload for demo
    resultsDashboard.classList.add('hidden');
    loadingScreen.classList.remove('hidden');
    progressBar.style.width = '0%';
    loadingPercentage.textContent = '0%';
    setTimeout(initLoading, 500);
});

// Sound effects function (browser policies may block this without user interaction)
function playSound(type) {
    // Using AudioContext for programmatically generated sounds
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    
    if (type === 'click') {
        // Create click sound
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.type = 'sine';
        oscillator.frequency.value = 800;
        gainNode.gain.value = 0.1;
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.start();
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.1);
        oscillator.stop(audioContext.currentTime + 0.1);
    } else if (type === 'achievement') {
        // Create achievement sound
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(500, audioContext.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.2);
        
        gainNode.gain.value = 0.1;
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.start();
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.3);
        oscillator.stop(audioContext.currentTime + 0.3);
    }
}

// Add click sound to buttons (only triggered after user interaction)
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('click', () => {
        try {
            playSound('click');
        } catch (e) {
            console.log('Audio not supported or blocked by browser policy');
        }
    });
});

// Fix canvas sizing on window resize
function resizeCanvas() {
    if (domainChart) {
        domainChart.width = domainChart.parentElement.clientWidth;
        domainChart.height = domainChart.parentElement.clientHeight;
        if (resultsDashboard && !resultsDashboard.classList.contains('hidden')) {
            renderDomainChart();
        }
    }
}

window.addEventListener('resize', resizeCanvas);

// Initialize on document load
document.addEventListener('DOMContentLoaded', () => {
    // Set canvas size
    if (domainChart) {
        domainChart.width = domainChart.parentElement.clientWidth;
        domainChart.height = domainChart.parentElement.clientHeight;
    }
    
    // Start loading animation
    initLoading();
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    // Escape key closes modal
    if (e.key === 'Escape' && !leaderboardModal.classList.contains('hidden')) {
        leaderboardModal.classList.add('hidden');
    }
});

// Add some accessibility features
function setupAccessibility() {
    // Make the domain chart elements focusable
    const legendItems = document.querySelectorAll('.legend-item');
    legendItems.forEach((item, index) => {
        item.setAttribute('tabindex', '0');
        item.setAttribute('role', 'button');
        item.setAttribute('aria-label', `View ${quizData.domainPerformance[index]?.domain || 'domain'} performance`);
        
        item.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                // Highlight corresponding segment
                const domain = quizData.domainPerformance[index];
                if (domain) {
                    const ctx = domainChart.getContext('2d');
                    const centerX = domainChart.width / 2;
                    const centerY = domainChart.height / 2;
                    
                    renderDomainChart();
                    
                    ctx.globalAlpha = 0.3;
                    ctx.beginPath();
                    ctx.moveTo(centerX, centerY);
                    ctx.arc(centerX, centerY, Math.min(centerX, centerY) * 0.9, domain.angles.start, domain.angles.end);
                    ctx.closePath();
                    ctx.fillStyle = 'white';
                    ctx.fill();
                    ctx.globalAlpha = 1;
                    
                    // Show domain info in an accessible way
                    alert(`${domain.domain}: ${domain.score}% score on ${domain.questions} questions`);
                }
            }
        });
    });
}

// Call setup after DOM is fully loaded
window.addEventListener('load', setupAccessibility);