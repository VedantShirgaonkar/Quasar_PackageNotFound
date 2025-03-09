// Sample data
const students = [
  { id: 1, name: "Alice Johnson", class: "class-10a", avatar: "AJ" },
  { id: 2, name: "Bob Smith", class: "class-10a", avatar: "BS" },
  { id: 3, name: "Charlie Brown", class: "class-10a", avatar: "CB" },
  { id: 4, name: "David Miller", class: "class-10b", avatar: "DM" },
  { id: 5, name: "Eva Williams", class: "class-10b", avatar: "EW" },
  { id: 6, name: "Frank Thomas", class: "class-10b", avatar: "FT" },
  { id: 7, name: "Grace Lee", class: "class-11a", avatar: "GL" },
  { id: 8, name: "Henry Clark", class: "class-11a", avatar: "HC" },
  { id: 9, name: "Ivy Robinson", class: "class-11a", avatar: "IR" },
  { id: 10, name: "Jack Davis", class: "class-11a", avatar: "JD" },
  { id: 11, name: "Karen Martinez", class: "class-10a", avatar: "KM" },
  { id: 12, name: "Leo Wilson", class: "class-10b", avatar: "LW" },
];

// Sample MCQs
const sampleMCQs = [
  {
    id: 1,
    question: "What is the primary function of mitochondria in a cell?",
    options: [
      { id: "a", text: "Protein synthesis", correct: false },
      { id: "b", text: "Energy production", correct: true },
      { id: "c", text: "Waste removal", correct: false },
      { id: "d", text: "Cell division", correct: false },
    ],
  },
  {
    id: 2,
    question:
      "Which organelle is responsible for protein synthesis in the cell?",
    options: [
      { id: "a", text: "Mitochondria", correct: false },
      { id: "b", text: "Golgi apparatus", correct: false },
      { id: "c", text: "Ribosomes", correct: true },
      { id: "d", text: "Lysosomes", correct: false },
    ],
  },
  {
    id: 3,
    question: "What is the function of chloroplasts in plant cells?",
    options: [
      { id: "a", text: "Respiration", correct: false },
      { id: "b", text: "Photosynthesis", correct: true },
      { id: "c", text: "Cell division", correct: false },
      { id: "d", text: "Protein synthesis", correct: false },
    ],
  },
];

document.addEventListener("DOMContentLoaded", function () {
  // DOM Elements
  const uploadArea = document.getElementById("upload-area");
  const fileInput = document.getElementById("file-input");
  const loadingAnimation = document.getElementById("loading-animation");
  const uploadedFileInfo = document.getElementById("uploaded-file-info");
  const fileNameText = document.getElementById("file-name-text");
  const generateBtn = document.getElementById("generate-btn");
  const questionList = document.getElementById("question-list");
  const noQuestionsMsg = document.getElementById("no-questions-msg");
  const selectAllBtn = document.getElementById("select-all-btn");
  const clearAllBtn = document.getElementById("clear-all-btn");
  const assignQuizBtn = document.getElementById("assign-quiz-btn");
  const studentList = document.getElementById("student-list");
  const classFilter = document.getElementById("class-filter");
  const modeToggle = document.getElementById("mode-toggle");
  const teacherView = document.getElementById("teacher-view");
  const studentView = document.getElementById("student-view");
  const toggleViewBtn = document.getElementById("toggle-view");
  const notification = document.getElementById("notification");
  const closeNotification = document.getElementById("close-notification");

  // Handle file upload
  uploadArea.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", handleFileUpload);

  function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
      uploadArea.style.display = "none";
      loadingAnimation.style.display = "block";

      // Simulate file processing
      setTimeout(() => {
        loadingAnimation.style.display = "none";
        uploadedFileInfo.style.display = "block";
        fileNameText.textContent = file.name;
        generateBtn.disabled = false;
      }, 2000);
    }
  }

  // Generate MCQs
  generateBtn.addEventListener("click", () => {
    noQuestionsMsg.style.display = "none";
    questionList.innerHTML = "";
    sampleMCQs.forEach((mcq) => {
      const questionItem = document.createElement("div");
      questionItem.classList.add("question-item");
      questionItem.innerHTML = `
                        <div class="question-header">
                            <div class="question-text">${mcq.question}</div>
                        </div>
                        <ul class="options-list">
                            ${mcq.options
                              .map(
                                (option) => `
                                <li class="option-item ${
                                  option.correct ? "correct" : ""
                                }">
                                    <div class="option-marker">${
                                      option.id
                                    }</div>
                                    <div class="option-text">${
                                      option.text
                                    }</div>
                                </li>
                            `
                              )
                              .join("")}
                        </ul>
                    `;
      questionList.appendChild(questionItem);
    });
  });

  // Populate students
  function populateStudents() {
    studentList.innerHTML = "";
    students.forEach((student) => {
      const studentItem = document.createElement("div");
      studentItem.classList.add("student-item");
      studentItem.dataset.class = student.class;
      studentItem.innerHTML = `
                        <div class="student-avatar">${student.avatar}</div>
                        <div class="student-name">${student.name}</div>
                    `;
      studentList.appendChild(studentItem);
    });
  }

  // Filter students by class
  classFilter.addEventListener("change", () => {
    const selectedClass = classFilter.value;
    const studentItems = studentList.querySelectorAll(".student-item");
    studentItems.forEach((item) => {
      if (selectedClass === "all" || item.dataset.class === selectedClass) {
        item.style.display = "block";
      } else {
        item.style.display = "none";
      }
    });
  });

  // Select all students
  selectAllBtn.addEventListener("click", () => {
    const studentItems = studentList.querySelectorAll(".student-item");
    studentItems.forEach((item) => item.classList.add("selected"));
    assignQuizBtn.disabled = false;
  });

  // Clear all selections
  clearAllBtn.addEventListener("click", () => {
    const studentItems = studentList.querySelectorAll(".student-item");
    studentItems.forEach((item) => item.classList.remove("selected"));
    assignQuizBtn.disabled = true;
  });

  // Toggle view
  modeToggle.addEventListener("click", () => {
    teacherView.style.display =
      teacherView.style.display === "none" ? "block" : "none";
    studentView.style.display =
      studentView.style.display === "none" ? "block" : "none";
  });

  toggleViewBtn.addEventListener("click", () => {
    teacherView.style.display =
      teacherView.style.display === "none" ? "block" : "none";
    studentView.style.display =
      studentView.style.display === "none" ? "block" : "none";
  });

  // Close notification
  closeNotification.addEventListener("click", () => {
    notification.style.display = "none";
  });

  // Initial population
  populateStudents();
});
