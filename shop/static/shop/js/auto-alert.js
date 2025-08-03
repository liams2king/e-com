// auto-alert.js
document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => {
                alert.remove();
            }, 500); // Délai pour supprimer après fondu
        }, 3000); // Affiche pendant 3s
    });
});


// This script fades out alerts after 4 seconds and removes them from the DOM after the fade-out transition completes.
// It applies to elements with the class 'alert' and uses a transition for a smooth effect.
// Make sure to include this script in your HTML after the alerts are rendered.