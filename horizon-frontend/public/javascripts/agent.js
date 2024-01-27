window.addEventListener('DOMContentLoaded', (event) => {
    const tabButtons = document.querySelectorAll('.pf-v5-c-tabs__link');
    const tabSections = document.querySelectorAll('.pf-v5-c-tab-content');

    tabButtons.forEach((button, index) => {
        button.addEventListener('click', () => {
            // Remove 'pf-m-current' class from all tabs
            tabButtons.forEach(btn => btn.parentElement.classList.remove('pf-m-current'));

            // Add 'pf-m-current' class to the clicked tab
            button.parentElement.classList.add('pf-m-current');

            // Hide all sections
            tabSections.forEach(section => section.setAttribute('hidden', 'hidden'));

            // Show the corresponding section
            tabSections[index].removeAttribute('hidden');
        });
    });
});