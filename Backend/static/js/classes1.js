// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all animations and charts
    initializePieCharts();
    initializeLineChart();
    initializeBarCharts();
    initializeLeaderboard();

    // Add event listeners
    addLeaderboardInteractivity();
});

// Sample data
const classData = {
    correctAnswers: 68,
    participation: 85,
    performanceTrend: [65, 68, 72, 70, 75, 78, 82],
    difficultyAnalysis: [
        { label: 'Quiz 1', value: 45 },
        { label: 'Quiz 2', value: 65 },
        { label: 'Quiz 3', value: 80 },
        { label: 'Quiz 4', value: 55 },
        { label: 'Quiz 5', value: 70 }
    ],
    topicPerformance: [
        { label: 'Algebra', value: 75 },
        { label: 'Geometry', value: 65 },
        { label: 'Calculus', value: 55 },
        { label: 'Statistics', value: 85 },
        { label: 'Physics', value: 70 }
    ],
    students: [
        { id: 1, name: 'Emma Johnson', score: 95, change: 'up', details: { quizzesTaken: 12, avgScore: 92, strengths: 'Algebra, Statistics', weaknesses: 'Calculus' } },
        { id: 2, name: 'Liam Smith', score: 92, change: 'up', details: { quizzesTaken: 12, avgScore: 89, strengths: 'Physics, Geometry', weaknesses: 'Statistics' } },
        { id: 3, name: 'Olivia Brown', score: 88, change: 'same', details: { quizzesTaken: 11, avgScore: 86, strengths: 'Calculus, Algebra', weaknesses: 'Geometry' } },
        { id: 4, name: 'Noah Wilson', score: 85, change: 'down', details: { quizzesTaken: 12, avgScore: 83, strengths: 'Statistics', weaknesses: 'Physics' } },
        { id: 5, name: 'Ava Martinez', score: 82, change: 'up', details: { quizzesTaken: 10, avgScore: 80, strengths: 'Geometry', weaknesses: 'Algebra' } },
        { id: 6, name: 'Ethan Davis', score: 78, change: 'down', details: { quizzesTaken: 11, avgScore: 76, strengths: 'Physics', weaknesses: 'Statistics' } },
        { id: 7, name: 'Sophia Taylor', score: 75, change: 'same', details: { quizzesTaken: 9, avgScore: 74, strengths: 'Algebra', weaknesses: 'Calculus' } },
        { id: 8, name: 'Mason Anderson', score: 72, change: 'up', details: { quizzesTaken: 10, avgScore: 70, strengths: 'Statistics', weaknesses: 'Physics' } }
    ]
};

// Initialize pie charts
function initializePieCharts() {
    // Correct vs Incorrect Answers Pie Chart
    const correctChart = document.getElementById('correctVsIncorrect');
    correctChart.style.background = `conic-gradient(
        #6e56CF 0% ${classData.correctAnswers}%, 
        #444444 ${classData.correctAnswers}% 100%
    )`;
    
    // Add animation
    correctChart.classList.add('scale-in');
    
    // Student Participation Pie Chart
    const participationChart = document.getElementById('participation');
    participationChart.style.background = `conic-gradient(
        #6e56CF 0% ${classData.participation}%, 
        #444444 ${classData.participation}% 100%
    )`;
    
    // Add animation
    participationChart.classList.add('scale-in');
}

// Initialize line chart
function initializeLineChart() {
    const lineChart = document.getElementById('performanceTrend');
    const data = classData.performanceTrend;
    const maxValue = Math.max(...data) * 1.2; // Add some padding
    
    // Clear previous content
    while (lineChart.children.length > 2) {
        lineChart.removeChild(lineChart.lastChild);
    }
    
    // Create points and lines
    for (let i = 0; i < data.length; i++) {
        const x = (i / (data.length - 1)) * 100;
        const y = 100 - (data[i] / maxValue) * 100;
        
        // Create point
        const point = document.createElement('div');
        point.className = 'line-point';
        point.style.left = `${x}%`;
        point.style.top = `${y}%`;
        point.setAttribute('data-value', data[i]);
        
        // Add tooltip on hover
        point.addEventListener('mouseover', function() {
            const tooltip = document.createElement('div');
            tooltip.style.position = 'absolute';
            tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
            tooltip.style.color = 'white';
            tooltip.style.padding = '5px 10px';
            tooltip.style.borderRadius = '4px';
            tooltip.style.fontSize = '12px';
            tooltip.style.zIndex = '10';
            tooltip.style.top = '-30px';
            tooltip.style.left = '50%';
            tooltip.style.transform = 'translateX(-50%)';
            tooltip.textContent = `Quiz ${i + 1}: ${data[i]}%`;
            this.appendChild(tooltip);
        });
        
        point.addEventListener('mouseout', function() {
            const tooltip = this.querySelector('div');
            if (tooltip) {
                this.removeChild(tooltip);
            }
        });
        
        lineChart.appendChild(point);
        
        // Create line segment (except for the last point)
        if (i < data.length - 1) {
            const nextX = ((i + 1) / (data.length - 1)) * 100;
            const nextY = 100 - (data[i + 1] / maxValue) * 100;
            
            const dx = nextX - x;
            const dy = nextY - y;
            const length = Math.sqrt(dx * dx + dy * dy);
            const angle = Math.atan2(dy, dx) * 180 / Math.PI;
            
            const line = document.createElement('div');
            line.className = 'line-segment';
            line.style.width = `${length}%`;
            line.style.left = `${x}%`;
            line.style.top = `${y}%`;
            line.style.transform = `rotate(${angle}deg)`;
            
            lineChart.appendChild(line);
        }
    }
    
    // Add x-axis labels
    for (let i = 0; i < data.length; i++) {
        const x = (i / (data.length - 1)) * 100;
        
        const label = document.createElement('div');
        label.className = 'bar-label';
        label.style.left = `${x}%`;
        label.style.bottom = '-25px';
        label.textContent = `Quiz ${i + 1}`;
        
        lineChart.appendChild(label);
    }
    
    // Animate points with delay
    const points = lineChart.querySelectorAll('.line-point');
    points.forEach((point, index) => {
        setTimeout(() => {
            point.style.opacity = '1';
            point.style.transform = 'translate(-50%, -50%) scale(1)';
        }, index * 100);
    });
    
    // Animate lines with delay
    const lines = lineChart.querySelectorAll('.line-segment');
    lines.forEach((line, index) => {
        setTimeout(() => {
            line.style.opacity = '1';
        }, index * 100 + 50);
    });
}

// Initialize bar charts
function initializeBarCharts() {
    // Difficulty Analysis Bar Chart
    const difficultyChart = document.getElementById('difficultyAnalysis');
    const difficultyContainer = difficultyChart.querySelector('.bar-container');
    const difficultyData = classData.difficultyAnalysis;
    
    // Clear previous content
    difficultyContainer.innerHTML = '';
    
    // Create bars
    difficultyData.forEach(item => {
        const barWrapper = document.createElement('div');
        barWrapper.style.flex = '1';
        barWrapper.style.display = 'flex';
        barWrapper.style.flexDirection = 'column';
        barWrapper.style.alignItems = 'center';
        
        const bar = document.createElement('div');
        bar.className = 'bar';
        bar.style.width = '100%';
        bar.style.height = '0';
        
        // Animate height after a delay
        setTimeout(() => {
            bar.style.height = `${item.value}%`;
        }, 300);
        
        const label = document.createElement('div');
        label.className = 'bar-label';
        label.textContent = item.label;
        
        // Add tooltip on hover
        bar.addEventListener('mouseover', function() {
            const tooltip = document.createElement('div');
            tooltip.style.position = 'absolute';
            tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
            tooltip.style.color = 'white';
            tooltip.style.padding = '5px 10px';
            tooltip.style.borderRadius = '4px';
            tooltip.style.fontSize = '12px';
            tooltip.style.zIndex = '10';
            tooltip.style.top = '-30px';
            tooltip.style.left = '50%';
            tooltip.style.transform = 'translateX(-50%)';
            tooltip.textContent = `Difficulty: ${item.value}%`;
            this.appendChild(tooltip);
        });
        
        bar.addEventListener('mouseout', function() {
            const tooltip = this.querySelector('div');
            if (tooltip) {
                this.removeChild(tooltip);
            }
        });
        
        barWrapper.appendChild(bar);
        barWrapper.appendChild(label);
        difficultyContainer.appendChild(barWrapper);
    });
    
    // Topic Performance Bar Chart
    const topicChart = document.getElementById('topicPerformance');
    const topicContainer = topicChart.querySelector('.bar-container');
    const topicData = classData.topicPerformance;
    
    // Clear previous content
    topicContainer.innerHTML = '';
    
    // Create bars
    topicData.forEach(item => {
        const barWrapper = document.createElement('div');
        barWrapper.style.flex = '1';
        barWrapper.style.display = 'flex';
        barWrapper.style.flexDirection = 'column';
        barWrapper.style.alignItems = 'center';
        
        const bar = document.createElement('div');
        bar.className = 'bar';
        bar.style.width = '100%';
        bar.style.height = '0';
        
        // Animate height after a delay
        setTimeout(() => {
            bar.style.height = `${item.value}%`;
        }, 300);
        
        const label = document.createElement('div');
        label.className = 'bar-label';
        label.textContent = item.label;
        
        // Add tooltip on hover
        bar.addEventListener('mouseover', function() {
            const tooltip = document.createElement('div');
            tooltip.style.position = 'absolute';
            tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
            tooltip.style.color = 'white';
            tooltip.style.padding = '5px 10px';
            tooltip.style.borderRadius = '4px';
            tooltip.style.fontSize = '12px';
            tooltip.style.zIndex = '10';
            tooltip.style.top = '-30px';
            tooltip.style.left = '50%';
            tooltip.style.transform = 'translateX(-50%)';
            tooltip.textContent = `Score: ${item.value}%`;
            this.appendChild(tooltip);
        });
        
        bar.addEventListener('mouseout', function() {
            const tooltip = this.querySelector('div');
            if (tooltip) {
                this.removeChild(tooltip);
            }
        });
        
        barWrapper.appendChild(bar);
        barWrapper.appendChild(label);
        topicContainer.appendChild(barWrapper);
    });
}

// Initialize leaderboard
function initializeLeaderboard() {
    const leaderboard = document.getElementById('leaderboard');
    
    // Clear previous content
    leaderboard.innerHTML = '';
    
    // Create leaderboard items
    classData.students.forEach((student, index) => {
        const item = document.createElement('li');
        item.className = `leaderboard-item fade-in`;
        item.setAttribute('data-student-id', student.id);
        
        // Add top-3 class for styling
        if (index < 3) {
            item.classList.add(`top-${index + 1}`);
            item.classList.add('top-3');
        }
        
        // Create rank element
        const rank = document.createElement('div');
        rank.className = 'rank';
        rank.textContent = index + 1;
        
        // Create student info element
        const info = document.createElement('div');
        info.className = 'student-info';
        
        const name = document.createElement('div');
        name.className = 'student-name';
        name.textContent = student.name;
        
        const score = document.createElement('div');
        score.className = 'student-score';
        score.textContent = `Score: ${student.score}%`;
        
        info.appendChild(name);
        info.appendChild(score);
        
        // Create rank change element
        const change = document.createElement('div');
        change.className = 'rank-change';
        
        if (student.change === 'up') {
            change.innerHTML = '&#9650; +2';
            change.classList.add('rank-up');
        } else if (student.change === 'down') {
            change.innerHTML = '&#9660; -1';
            change.classList.add('rank-down');
        } else {
            change.innerHTML = '&#9679;';
            change.classList.add('rank-same');
        }
        
        // Append elements to item
        item.appendChild(rank);
        item.appendChild(info);
        item.appendChild(change);
        
        // Create student details element (hidden by default)
        const details = document.createElement('div');
        details.className = 'student-details';
        details.id = `details-${student.id}`;
        
        const detailGrid = document.createElement('div');
        detailGrid.className = 'detail-grid';
        
        // Create detail items
        const quizzesTaken = createDetailItem('Quizzes Taken', student.details.quizzesTaken);
        const avgScore = createDetailItem('Average Score', `${student.details.avgScore}%`);
        const strengths = createDetailItem('Strengths', student.details.strengths);
        const weaknesses = createDetailItem('Weaknesses', student.details.weaknesses);
        
        // Create progress bar
        const progressContainer = document.createElement('div');
        progressContainer.style.gridColumn = 'span 2';
        progressContainer.style.marginTop = '1rem';
        
        const progressLabel = document.createElement('div');
        progressLabel.className = 'detail-label';
        progressLabel.textContent = 'Overall Progress';
        
        const progressBar = document.createElement('div');
        progressBar.className = 'progress-bar';
        
        const progressFill = document.createElement('div');
        progressFill.className = 'progress-fill';
        progressFill.style.width = '0';
        
        // Animate progress bar when details are shown
        setTimeout(() => {
            progressFill.style.width = `${student.score}%`;
        }, 300);
        
        progressBar.appendChild(progressFill);
        progressContainer.appendChild(progressLabel);
        progressContainer.appendChild(progressBar);
        
        // Append detail items to grid
        detailGrid.appendChild(quizzesTaken);
        detailGrid.appendChild(avgScore);
        detailGrid.appendChild(strengths);
        detailGrid.appendChild(weaknesses);
        detailGrid.appendChild(progressContainer);
        
        details.appendChild(detailGrid);
        
        // Append details to leaderboard
        leaderboard.appendChild(item);
        leaderboard.appendChild(details);
    });
}

// Helper function to create detail item
function createDetailItem(label, value) {
    const item = document.createElement('div');
    item.className = 'detail-item';
    
    const labelEl = document.createElement('div');
    labelEl.className = 'detail-label';
    labelEl.textContent = label;
    
    const valueEl = document.createElement('div');
    valueEl.className = 'detail-value';
    valueEl.textContent = value;
    
    item.appendChild(labelEl);
    item.appendChild(valueEl);
    
    return item;
}

// Add interactivity to leaderboard
function addLeaderboardInteractivity() {
    const leaderboardItems = document.querySelectorAll('.leaderboard-item');
    
    leaderboardItems.forEach(item => {
        item.addEventListener('click', function() {
            const studentId = this.getAttribute('data-student-id');
            const details = document.getElementById(`details-${studentId}`);
            
            // Toggle active class
            if (details.classList.contains('active')) {
                details.classList.remove('active');
            } else {
                // Close any open details
                document.querySelectorAll('.student-details.active').forEach(el => {
                    el.classList.remove('active');
                });
                
                // Open this detail
                details.classList.add('active');
                
                // Update charts based on selected student
                updateChartsForStudent(studentId);
            }
        });
    });
}

// Update charts based on selected student
function updateChartsForStudent(studentId) {
    // Find student data
    const student = classData.students.find(s => s.id == studentId);
    
    if (!student) return;
    
    // Simulate updating charts with student-specific data
    // In a real application, you would have actual student-specific data
    
    // Update pie charts with animation
    const correctChart = document.getElementById('correctVsIncorrect');
    correctChart.style.transform = 'scale(0.8)';
    
    setTimeout(() => {
        // Generate random value between 60-90 for demo purposes
        const correctValue = Math.floor(Math.random() * 30) + 60;
        
        correctChart.style.background = `conic-gradient(
            #6e56CF 0% ${correctValue}%, 
            #444444 ${correctValue}% 100%
        )`;
        
        correctChart.querySelector('.percentage').textContent = `${correctValue}%`;
        correctChart.style.transform = 'scale(1)';
    }, 300);
    
    // Update bar charts
    const difficultyBars = document.querySelectorAll('#difficultyAnalysis .bar');
    difficultyBars.forEach(bar => {
        // Generate random value between 40-90 for demo purposes
        const newHeight = Math.floor(Math.random() * 50) + 40;
        bar.style.height = '10%';
        
        setTimeout(() => {
            bar.style.height = `${newHeight}%`;
        }, 300);
    });
    
    const topicBars = document.querySelectorAll('#topicPerformance .bar');
    topicBars.forEach(bar => {
        // Generate random value between 40-90 for demo purposes
        const newHeight = Math.floor(Math.random() * 50) + 40;
        bar.style.height = '10%';
        
        setTimeout(() => {
            bar.style.height = `${newHeight}%`;
        }, 300);
    });
    
    // Update line chart
    const linePoints = document.querySelectorAll('#performanceTrend .line-point');
    const lineSegments = document.querySelectorAll('#performanceTrend .line-segment');
    
    // Hide points and lines
    linePoints.forEach(point => {
        point.style.opacity = '0';
    });
    
    lineSegments.forEach(line => {
        line.style.opacity = '0';
    });
    
    // Generate new random data for demo purposes
    setTimeout(() => {
        const newData = [];
        for (let i = 0; i < linePoints.length; i++) {
            newData.push(Math.floor(Math.random() * 30) + 60);
        }
        
        const maxValue = Math.max(...newData) * 1.2;
        
        // Update points
        linePoints.forEach((point, i) => {
            const y = 100 - (newData[i] / maxValue) * 100;
            point.style.top = `${y}%`;
            point.setAttribute('data-value', newData[i]);
            point.style.opacity = '1';
        });
        
        // Update line segments
        lineSegments.forEach((line, i) => {
            const x1 = (i / (newData.length - 1)) * 100;
            const y1 = 100 - (newData[i] / maxValue) * 100;
            const x2 = ((i + 1) / (newData.length - 1)) * 100;
            const y2 = 100 - (newData[i + 1] / maxValue) * 100;
            
            const dx = x2 - x1;
            const dy = y2 - y1;
            const length = Math.sqrt(dx * dx + dy * dy);
            const angle = Math.atan2(dy, dx) * 180 / Math.PI;
            
            line.style.width = `${length}%`;
            line.style.left = `${x1}%`;
            line.style.top = `${y1}%`;
            line.style.transform = `rotate(${angle}deg)`;
            line.style.opacity = '1';
        });
    }, 500);
}
