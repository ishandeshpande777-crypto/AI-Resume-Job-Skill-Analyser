const form = document.getElementById("resumeForm");

if (form) {

    form.addEventListener("submit", function(event) {

        const resume = document.getElementById("resume");

        const jobDescription =
            document.getElementById("job_description");

        if (!resume.files.length) {
            alert("Please upload your resume.");
            event.preventDefault();
            return;
        }

        if (!resume.files[0].name.toLowerCase().endsWith(".pdf")) {
            alert("Please select a PDF file.");
            event.preventDefault();
            return;
        }

        if (!jobDescription.value.trim()) {
            alert("Please enter a job description.");
            event.preventDefault();
            return;
        }

        const button = document.getElementById("analyzeBtn");

        button.innerText = "Analysing Resume...";
        button.disabled = true;

    });

}

