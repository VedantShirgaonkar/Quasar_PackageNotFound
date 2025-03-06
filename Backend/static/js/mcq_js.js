let selectedAnswer = null;
        let timeLeft = 30;
        const timerText = document.querySelector(".timer-text");
        const progressCircle = document.querySelector(".progress-ring-circle");

        const startTimer = () => {
            let circumference = 251;
            let offset = 0;
            const timerInterval = setInterval(() => {
                if (timeLeft <= 0) {
                    clearInterval(timerInterval);
                    return;
                }
                timeLeft--;
                offset = circumference - (timeLeft / 30) * circumference;
                progressCircle.style.strokeDashoffset = offset;
                timerText.innerText = timeLeft;
            }, 1000);
        };

        startTimer();



        document.querySelectorAll(".answer").forEach((answer) => {
            answer.addEventListener("click", () => {
                // Reset only previously selected answer
                document.querySelectorAll(".answer").forEach((ans) => ans.classList.remove("selected"));

                // Mark selected answer
                answer.classList.add("selected");
                selectedAnswer = answer;

                // Enable submit button
                document.querySelector(".submit-btn").disabled = false;
            });
        });

        document.querySelector(".submit-btn").addEventListener("click", () => {
            if (!selectedAnswer) return; // Prevent submission if no answer is selected

            // Highlight the selected answer based on correctness
            if (selectedAnswer.dataset.correct === "true") {
                selectedAnswer.classList.add("correct"); // Green if correct
            } else {
                selectedAnswer.classList.add("incorrect"); // Red if incorrect
                // Also mark the correct answer green
                document.querySelector('[data-correct="true"]').classList.add("correct");
            }

            // Disable submit button and enable next button
            document.querySelector(".submit-btn").disabled = true;
            document.querySelector(".next-btn").disabled = false;
        });

        document.querySelector(".next-btn").addEventListener("click", () => {
            console.log("Next question logic here...");
        });