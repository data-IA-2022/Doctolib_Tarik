    // Change the date list based on the selected patient
    document.getElementById('patient_select').addEventListener('change', function() {
        var patientId = this.value;
        fetch(`/get-dates-for-patient/${patientId}`)
            .then(response => response.json())
            .then(data => {
                var dateSelect = document.getElementById('date_select');
                dateSelect.innerHTML = ''; // Clear existing options
                data.dates.forEach(function(date) {
                    var option = new Option(date, date);
                    dateSelect.add(option);
                });
            });
    });
    
    // Handle multi-step form navigation
    document.addEventListener("DOMContentLoaded", function() {
        let currentStep = 1;
        const formSteps = document.querySelectorAll('.form-step');
        const nextButtons = document.querySelectorAll('.next');
        const prevButtons = document.querySelectorAll('.prev');
        const progressBar = document.querySelector('.progress-bar');
        const totalSteps = formSteps.length;
    
        // Function to update progress bar
        function updateProgressBar(step) {
            const progressPercentage = (step / totalSteps) * 100;
            progressBar.style.width = progressPercentage + '%';
        }
    
        // Initialize progress bar
        updateProgressBar(currentStep);
    
        // Hide all steps except the first one
        formSteps.forEach((step, index) => {
            if (index !== 0) {
                step.classList.remove('active');
            }
        });
    
        // Function to move to a specific step
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
    
        // Next button event listeners
        nextButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                if (currentStep < totalSteps) {
                    moveToStep(currentStep + 1);
                }
            });
        });
    
        // Previous button event listeners
        prevButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                if (currentStep > 1) {
                    moveToStep(currentStep - 1);
                }
            });
        });
    });
    function confirmDelete() {
        if (confirm("Are you sure you want to delete this record?")) {
            document.querySelector('input[name="action"]').value = 'delete';
            document.getElementById('crud_form_sante').submit();
        }
    }