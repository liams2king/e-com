document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("user-dropdown-toggle");
  const dropdown = document.getElementById("user-dropdown");

  toggleBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    dropdown.classList.toggle("show");
  });

  document.addEventListener("click", function () {
    dropdown.classList.remove("show");
  });
});
