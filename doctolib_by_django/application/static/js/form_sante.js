document.addEventListener("DOMContentLoaded", function() {
  let currentStep = 1;  // We start with step 1

  const formSteps = document.querySelectorAll('.form-step');
  const nextButtons = document.querySelectorAll('.next');
  const prevButtons = document.querySelectorAll('.prev');

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

      // Update currentStep value
      currentStep = step;
  }
});