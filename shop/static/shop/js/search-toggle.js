document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('search-toggle');
  const searchForm = document.getElementById('search-form');

  if (toggleBtn && searchForm) {
    toggleBtn.addEventListener('click', function () {
      if (searchForm.style.display === 'none' || searchForm.style.display === '') {
        searchForm.style.display = 'inline-flex'; // tu peux mettre 'block' si tu préfères
        searchForm.querySelector('input').focus();
      } else {
        searchForm.style.display = 'none';
      }
    });
  }
});


document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('search-toggle');
  const searchForm = document.getElementById('search-form-container');

  toggleBtn.addEventListener('click', function () {
    searchForm.classList.toggle('hidden');
  });
});
