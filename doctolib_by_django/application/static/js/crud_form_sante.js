// change la liste de date en fonction du patient select
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
