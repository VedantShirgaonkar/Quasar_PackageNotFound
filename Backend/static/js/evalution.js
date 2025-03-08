
       
        // Animate number counting up
        function animateCounter(element, target, duration) {
            let start = 0;
            const increment = target / (duration / 16);
            const timer = setInterval(() => {
                start += increment;
                element.textContent = Math.floor(start);
                if (start >= target) {
                    element.textContent = target;
                    clearInterval(timer);
                }
            }, 16);
        }
        
        // Format seconds into MM:SS
        function formatTime(seconds) {
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
        }
        
        // Create confetti effect for high scores
        function createConfetti() {
            const confettiCount = 100;
            const colors = ['#6e56cf', '#9b59b6', '#4cd137', '#e84118', '#ffffff'];
            
            for (let i = 0; i < confettiCount; i++) {
                const confetti = document.createElement('div');
                confetti.className = 'confetti';
                confetti.style.left = Math.random() * 100 + 'vw';
                confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.width = Math.random() * 10 + 5 + 'px';
                confetti.style.height = Math.random() * 10 + 5 + 'px';
                confetti.style.animationDuration = Math.random() * 3 + 2 + 's';
                confetti.style.animationDelay = Math.random() * 2 + 's';
                document.body.appendChild(confetti);
                
                // Remove confetti after animation
                setTimeout(() => {
                    confetti.remove();
                }, 5000);
            }
        }
        
        // Display performance message and emoji
        function setPerformanceMessage(accuracy) {
            const messageBox = document.getElementById('message-box');
            const badge = document.getElementById('performance-badge');
            
            if (accuracy >= 80) {
                messageBox.textContent = "Awesome! You're a Quiz Champion! 🏆";
                badge.textContent = "🎉";
                setTimeout(createConfetti, 1000);
            } else if (accuracy >= 50) {
                messageBox.textContent = "Good job! Keep improving! 🚀";
                badge.textContent = "😐";
            } else {
                messageBox.textContent = "Keep Practicing! You got this! 💪";
                badge.textContent = "😢";
            }
        }
        
        // Initialize the page with quiz data
        function initializePage() {
            // Set values with animations
            setTimeout(() => {
                animateCounter(document.getElementById('total-score'), quizData.score, 1500);
                document.getElementById('score-bar').style.transform = `scaleX(${quizData.score / quizData.maxScore})`;
                
                animateCounter(document.getElementById('accuracy-text'), quizData.accuracy, 1500);
                document.getElementById('accuracy-circle').style.background = `conic-gradient(var(--primary-color) ${quizData.accuracy}%, transparent 0%)`;
                
                animateCounter(document.getElementById('correct-count'), quizData.correctCount, 1000);
                animateCounter(document.getElementById('incorrect-count'), quizData.incorrectCount, 1000);
                
                const totalQuestions = quizData.correctCount + quizData.incorrectCount;
                document.getElementById('correct-bar').style.width = `${(quizData.correctCount / totalQuestions) * 100}%`;
                document.getElementById('incorrect-bar').style.width = `${(quizData.incorrectCount / totalQuestions) * 100}%`;
                
                //document.getElementById('time-taken').textContent = formatTime(quizData.timeTaken);
                document.getElementById('time-taken').textContent = quizData.timeTaken;

                setPerformanceMessage(quizData.accuracy);
            }, 500);
            
            // Populate questions
            const questionsContainer = document.getElementById('questions-container');
            quizData.questions.forEach((question, index) => {
                const questionCard = document.createElement('div');
                questionCard.className = 'question-card';
                questionCard.style.setProperty('--i', index);
                
                const cardInner = document.createElement('div');
                cardInner.className = 'card-inner';
                
                const cardFront = document.createElement('div');
                cardFront.className = 'card-front';
                
                const resultSpan = document.createElement('span');
                resultSpan.className = `card-result ${question.isCorrect ? 'correct' : 'incorrect'}`;
                resultSpan.textContent = question.isCorrect ? '✓' : '✗';
                
                const questionText = document.createElement('span');
                questionText.textContent = question.question;
                
                cardFront.appendChild(resultSpan);
                cardFront.appendChild(questionText);
                
                const cardBack = document.createElement('div');
                cardBack.className = 'card-back';
                cardBack.innerHTML = `
                    <div style="width: 100%;">
                        <p><strong>Your answer:</strong> ${question.yourAnswer}</p>
                        <p><strong>Correct answer:</strong> ${question.correctAnswer}</p>
                    </div>
                `;
                
                cardInner.appendChild(cardFront);
                cardInner.appendChild(cardBack);
                questionCard.appendChild(cardInner);
                
                // Add click event to flip card
                questionCard.addEventListener('click', () => {
                    questionCard.classList.toggle('flipped');
                });
                
                questionsContainer.appendChild(questionCard);
            });
            
            // Add event listener to retry button
            document.getElementById('retry-btn').addEventListener('click', function() {
                this.classList.add('clicked');
                setTimeout(() => {
                    alert('Starting a new quiz!');
                    // In a real application, this would redirect to a new quiz
                }, 300);
            });
        }
        
        // Initialize when page loads
        window.addEventListener('load', initializePage);