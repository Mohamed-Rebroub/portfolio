document.getElementById("chatToggle").addEventListener("click", function () {
  const chatWidget = document.getElementById("chatWidget");
  const chatToggle = document.getElementById("chatToggle");

  // Bascule la classe 'active' pour afficher/masquer le widget
  chatWidget.classList.toggle("active");
  chatToggle.classList.toggle("active");

  // Focaliser sur le champ d'entrée quand le widget est ouvert
  if (chatWidget.classList.contains("active")) {
    document.getElementById("message").focus();
  }
});

// Fermer le widget si l'utilisateur clique en dehors
document.addEventListener("click", function (e) {
  const chatWidget = document.getElementById("chatWidget");
  const chatToggle = document.getElementById("chatToggle");

  // Vérifie si le clic est en dehors du widget et du bouton
  if (
    !chatWidget.contains(e.target) &&
    !chatToggle.contains(e.target) &&
    chatWidget.classList.contains("active")
  ) {
    chatWidget.classList.remove("active");
    chatToggle.classList.remove("active");
  }
});
