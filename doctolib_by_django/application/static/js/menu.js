document.querySelectorAll('.dropdown-toggle').forEach(toggle => {
  toggle.addEventListener('mouseenter', function() {
      this.nextElementSibling.style.display = 'block';
  });
  toggle.addEventListener('mouseleave', function() {
      this.nextElementSibling.style.display = 'none';
  });
});

window.addEventListener('resize', function() {
  const nav = document.querySelector('[x-data]');
  if (window.innerWidth > 768) {  // Assuming 768px is your breakpoint for md in TailwindCSS
      nav.setAttribute('x-data', '{ open: false }');
  }
});