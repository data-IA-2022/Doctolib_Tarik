document.addEventListener("DOMContentLoaded", function() {
    let currentStep = 1;  // Start with step 1
  
    const formSteps = document.querySelectorAll('.form-step');
    const nextButtons = document.querySelectorAll('.next');
    const prevButtons = document.querySelectorAll('.prev');
    const progressBar = document.querySelector('.progress-bar');
  
    // Function to update progress bar
    function updateProgressBar(step) {
        const totalSteps = formSteps.length;
        const progressPercentage = (step / totalSteps) * 100;
        progressBar.style.width = progressPercentage + '%';
    }
  
    // Initialize progress bar
    updateProgressBar(currentStep);
  
    // Hide all steps except the first one
    formSteps.forEach((step, index) => {
        if(index !== 0) {
            step.classList.remove('active');
        }
    });
  
    nextButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            if(currentStep < formSteps.length) {
                moveToStep(currentStep + 1);
            }
        });
    });
  
    prevButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            if(currentStep > 1) {
                moveToStep(currentStep - 1);
            }
        });
    });
  
    function moveToStep(step) {
        // Hide current step
        document.querySelector(`.form-step[data-step="${currentStep}"]`).classList.remove('active');
  
        // Show next step
        document.querySelector(`.form-step[data-step="${step}"]`).classList.add('active');
  
        // Update progress bar
        updateProgressBar(step);
  
        // Update currentStep value
        currentStep = step;
    }
  });
  