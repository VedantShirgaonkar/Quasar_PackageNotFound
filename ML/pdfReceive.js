const fileInput = document.getElementById("pdf-upload");

fileInput.addEventListener("change", async (event) => {
    const file = event.target.files[0];  
    if (!file) return;

    const formData = new FormData();
    formData.append("pdf", file);  

    const response = await fetch("http://localhost:3000/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();
    console.log("MCQs Generated:", data.mcqs);
});