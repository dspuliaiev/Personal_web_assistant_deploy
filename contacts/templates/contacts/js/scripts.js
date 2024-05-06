window.addEventListener('DOMContentLoaded', event => {
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

    const navLinks = document.querySelectorAll('.nav-link[data-bs-toggle="collapse"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('data-bs-target');
            if (target) {
                const collapse = document.querySelector(target);
                if (collapse) {
                    collapse.classList.toggle('show');
                    this.querySelector('.sb-sidenav-collapse-arrow').classList.toggle('show');
                }
            }
        });
    });
});