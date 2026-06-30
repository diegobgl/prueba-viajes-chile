// Bootstrap JS: tooltips para botones de las tarjetas.
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(
  (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
);

const navbar = document.querySelector(".navbar");
const contactForm = document.querySelector(".contact-form");

window.addEventListener("scroll", () => {
  navbar.classList.toggle("scrolled", window.scrollY > 80);
});

contactForm.addEventListener("submit", (event) => {
  event.preventDefault();
  alert("Gracias por contactarnos. Te responderemos pronto.");
  contactForm.reset();
});
