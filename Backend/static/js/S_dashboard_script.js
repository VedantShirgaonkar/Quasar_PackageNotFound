 // Student Data
/* const studentData = {
    name: "Jessica Smith",
    email: "jessica.smith@university.edu",
    institution: "University of Technology",
    grade: "Junior (Year 3)",
    stats: {
        mcqsAttempted: 487,
        accuracyPercentage: 76.4,
        avgTime: 42,
        studyStreak: 8
    }
};*/

document.addEventListener("DOMContentLoaded", () => {
    function animateNumber(element, start, end, duration) {
        let range = end - start;
        let increment = range / (duration / 10);
        let current = start;
        
        let timer = setInterval(() => {
            current += increment;
            if (current >= end) {
                current = end;
                clearInterval(timer);
            }
            element.textContent = Math.round(current);
        }, 10);
    }

    animateNumber(document.getElementById("mcqs-attempted"), 0, studentData.stats.mcqsAttempted, 1000);
    animateNumber(document.getElementById("accuracy-percentage"), 0, studentData.stats.accuracyPercentage, 1000);
    animateNumber(document.getElementById("avg-time"), 0, studentData.stats.avgTime, 1000);
    animateNumber(document.getElementById("study-streak"), 0, studentData.stats.studyStreak, 1000);
});


// Performance Data
const performanceData = {
    accuracyTrend: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
        values: [65, 70, 68, 74, 79, 75, 80, 82, 85]
    },
    topicStrengths: {
        labels: ['Algebra', 'Calculus', 'Statistics', 'Geometry', 'Probability', 'Trigonometry'],
        values: [85, 70, 90, 65, 75, 60]
    },
    topicPerformance: {
        labels: ['Algebra', 'Calculus', 'Statistics', 'Geometry', 'Probability', 'Trigonometry'],
        values: [85, 70, 90, 65, 75, 60]
    }
};

// Leaderboard Data
const leaderboardData = [
    { rank: 1, name: "Alex Johnson", accuracy: 92.7, questions: 512, progress: 95 },
    { rank: 2, name: "Sophia Chen", accuracy: 88.3, questions: 498, progress: 90 },
    { rank: 3, name: "Marcus Lee", accuracy: 85.1, questions: 531, progress: 87 },
    { rank: 4, name: "Jessica Smith", accuracy: 76.4, questions: 487, progress: 80 },
    { rank: 5, name: "Ryan Williams", accuracy: 74.9, questions: 456, progress: 78 },
    { rank: 6, name: "Olivia Garcia", accuracy: 72.1, questions: 422, progress: 75 },
    { rank: 7, name: "Daniel Kim", accuracy: 70.6, questions: 410, progress: 72 },
];

// Load student data
document.getElementById('student-name').textContent = studentData.name;
document.getElementById('initial').textContent = studentData.name.charAt(0).toUpperCase();

document.getElementById('student-email').textContent = studentData.email;
document.getElementById('student-institution').textContent = studentData.institution;
document.getElementById('student-grade').textContent = `Grade: ${studentData.grade}`;

document.getElementById('mcqs-attempted').textContent = studentData.stats.mcqsAttempted;
document.getElementById('accuracy-percentage').textContent = `${studentData.stats.accuracyPercentage}%`;
document.getElementById('avg-time').textContent = studentData.stats.avgTime;
document.getElementById('study-streak').textContent = studentData.stats.studyStreak;

// Load leaderboard data
const leaderboardBody = document.getElementById('leaderboard-body');
leaderboardData.forEach(user => {
    const row = document.createElement('tr');
    
    const rankCell = document.createElement('td');
    const rankDiv = document.createElement('div');
    rankDiv.className = `rank ${user.rank <= 3 ? 'top' : ''}`;
    rankDiv.textContent = user.rank;
    rankCell.appendChild(rankDiv);
    
    const nameCell = document.createElement('td');
    nameCell.textContent = user.name;
    if (user.name === studentData.name) {
        nameCell.style.fontWeight = 'bold';
        nameCell.style.color = 'var(--accent-color-light)';
    }
    
    const accuracyCell = document.createElement('td');
    accuracyCell.textContent = `${user.accuracy}%`;
    
    const questionsCell = document.createElement('td');
    questionsCell.textContent = user.questions;
    
    const progressCell = document.createElement('td');
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    const progressFill = document.createElement('div');
    progressFill.className = 'progress-fill';
    progressFill.style.width = `${user.progress}%`;
    progressBar.appendChild(progressFill);
    progressCell.appendChild(progressBar);
    
    row.appendChild(rankCell);
    row.appendChild(nameCell);
    row.appendChild(accuracyCell);
    row.appendChild(questionsCell);
    row.appendChild(progressCell);
    
    leaderboardBody.appendChild(row);
});

// Canvas drawing functions
function drawAccuracyTrendChart() {
    const canvas = document.getElementById('accuracy-trend-chart');
    const ctx = canvas.getContext('2d');
    
    // Set canvas size with correct scaling
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
    
    const data = performanceData.accuracyTrend;
    const padding = 40;
    const chartWidth = canvas.width - padding * 2;
    const chartHeight = canvas.height - padding * 2;
    
    // Draw background
    ctx.fillStyle = 'transparent';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw title
    ctx.fillStyle = '#ffffff';
    ctx.font = '16px Segoe UI';
    ctx.textAlign = 'center';
    ctx.fillText('Accuracy Trend Over Time', canvas.width / 2, padding / 2);
    
    // Draw axes
    ctx.strokeStyle = '#444444';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();
    
    // Draw labels
    ctx.fillStyle = '#b3b3b3';
    ctx.font = '12px Segoe UI';
    ctx.textAlign = 'center';
    
    // X-axis labels
    const xStep = chartWidth / (data.labels.length - 1);
    data.labels.forEach((label, i) => {
        const x = padding + i * xStep;
        ctx.fillText(label, x, canvas.height - padding + 20);
    });
    
    // Y-axis labels
    ctx.textAlign = 'right';
    for (let i = 0; i <= 5; i++) {
        const y = canvas.height - padding - (i * chartHeight / 5);
        const value = 50 + i * 10;
        ctx.fillText(`${value}%`, padding - 10, y + 5);
        
        // Grid lines
        ctx.strokeStyle = '#333333';
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(canvas.width - padding, y);
        ctx.stroke();
    }
    
    // Plot data points
    const minValue = 50;
    const maxValue = 100;
    const range = maxValue - minValue;
    
    // Draw line
    ctx.strokeStyle = '#7c4dff';
    ctx.lineWidth = 3;
    ctx.beginPath();
    
    data.values.forEach((value, i) => {
        const x = padding + i * xStep;
        const y = canvas.height - padding - ((value - minValue) / range * chartHeight);
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.stroke();
    
    // Draw gradient area under the line
    const gradient = ctx.createLinearGradient(0, padding, 0, canvas.height - padding);
    gradient.addColorStop(0, 'rgba(124, 77, 255, 0.5)');
    gradient.addColorStop(1, 'rgba(124, 77, 255, 0.05)');
    
    ctx.fillStyle = gradient;
    ctx.beginPath();
    
    data.values.forEach((value, i) => {
        const x = padding + i * xStep;
        const y = canvas.height - padding - ((value - minValue) / range * chartHeight);
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.lineTo(padding + (data.values.length - 1) * xStep, canvas.height - padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.closePath();
    ctx.fill();
    
    // Draw data points
    ctx.fillStyle = '#7c4dff';
    data.values.forEach((value, i) => {
        const x = padding + i * xStep;
        const y = canvas.height - padding - ((value - minValue) / range * chartHeight);
        
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = '#121212';
        ctx.beginPath();
        ctx.arc(x, y, 2, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = '#7c4dff';
    });
}

function drawRadarChart() {
    const canvas = document.getElementById('radar-chart');
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
    
    const data = performanceData.topicStrengths;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 30;
    
    // Draw background
    ctx.fillStyle = 'transparent';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw radar background
    const sides = data.labels.length;
    const angleStep = (Math.PI * 2) / sides;
    
    // Draw concentric circles and labels
    for (let level = 1; level <= 5; level++) {
        const levelRadius = radius * (level / 5);
        
        // Draw level circle
        ctx.strokeStyle = '#333333';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(centerX, centerY, levelRadius, 0, Math.PI * 2);
        ctx.stroke();
        
        // Draw level label on the first vertical axis
        if (level < 5) {
            ctx.fillStyle = '#777777';
            ctx.font = '10px Segoe UI';
            ctx.textAlign = 'left';
            ctx.fillText(`${level * 20}`, centerX + 5, centerY - levelRadius + 10);
        }
    }
    
    // Draw axes
    for (let i = 0; i < sides; i++) {
        const angle = i * angleStep - Math.PI / 2;
        const x = centerX + radius * Math.cos(angle);
        const y = centerY + radius * Math.sin(angle);
        
        ctx.strokeStyle = '#444444';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(x, y);
        ctx.stroke();
        
        // Draw axis label
        ctx.fillStyle = '#b3b3b3';
        ctx.font = '10px Segoe UI';
        ctx.textAlign = 'center';
        
        const labelX = centerX + (radius + 20) * Math.cos(angle);
        const labelY = centerY + (radius + 20) * Math.sin(angle);
        
        ctx.fillText(data.labels[i], labelX, labelY);
    }
    
    // Plot data points
    ctx.beginPath();
    
    data.values.forEach((value, i) => {
        const angle = i * angleStep - Math.PI / 2;
        const scaledRadius = (value / 100) * radius;
        const x = centerX + scaledRadius * Math.cos(angle);
        const y = centerY + scaledRadius * Math.sin(angle);
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.closePath();
    ctx.strokeStyle = '#7c4dff';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    ctx.fillStyle = 'rgba(124, 77, 255, 0.2)';
    ctx.fill();
    
    // Draw data points
    data.values.forEach((value, i) => {
        const angle = i * angleStep - Math.PI / 2;
        const scaledRadius = (value / 100) * radius;
        const x = centerX + scaledRadius * Math.cos(angle);
        const y = centerY + scaledRadius * Math.sin(angle);
        
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, Math.PI * 2);
        ctx.fillStyle = '#7c4dff';
        ctx.fill();
    });
}

function drawBarChart() {
    const canvas = document.getElementById('bar-chart');
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
    
    const data = performanceData.topicPerformance;
    const padding = 40;
    const chartWidth = canvas.width - padding * 2;
    const chartHeight = canvas.height - padding * 2;
    
    // Draw background
    ctx.fillStyle = 'transparent';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw axes
    ctx.strokeStyle = '#444444';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();
    
    // Draw horizontal grid lines and y-axis labels
    ctx.textAlign = 'right';
    ctx.fillStyle = '#b3b3b3';
    ctx.font = '10px Segoe UI';
    
    for (let i = 0; i <= 5; i++) {
        const y = canvas.height - padding - (i * chartHeight / 5);
        const value = i * 20;
        
        // Grid line
        ctx.strokeStyle = '#333333';
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(canvas.width - padding, y);
        ctx.stroke();
        
        // Label
        ctx.fillText(`${value}%`, padding - 5, y + 3);
    }
    
    // Draw bars
    const barWidth = chartWidth / data.labels.length - 10;
    
    data.values.forEach((value, i) => {
        const x = padding + i * (chartWidth / data.labels.length) + 5;
        const barHeight = (value / 100) * chartHeight;
        const y = canvas.height - padding - barHeight;
        
        // Create gradient for bar
        const gradient = ctx.createLinearGradient(x, y, x, canvas.height - padding);
        gradient.addColorStop(0, '#9e7dff');
        gradient.addColorStop(1, '#7c4dff');
        
        ctx.fillStyle = gradient;
        ctx.fillRect(x, y, barWidth, barHeight);
        
        // Bar value
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.font = '10px Segoe UI';
        ctx.fillText(`${value}%`, x + barWidth / 2, y - 5);
        
        // Bar label
        ctx.fillStyle = '#b3b3b3';
        ctx.fillText(data.labels[i], x + barWidth / 2, canvas.height - padding + 15);
    });
}

// Initialize charts when page loads
window.addEventListener('load', () => {
    drawAccuracyTrendChart();
    drawRadarChart();
    drawBarChart();
});

// Redraw charts on window resize
window.addEventListener('resize', () => {
    drawAccuracyTrendChart();
    drawRadarChart();
    drawBarChart();
});
