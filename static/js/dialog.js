// export to index

document.addEventListener("DOMContentLoaded", function () {

  // ========= 展開回答 =========
  const questions = document.querySelectorAll('.respond .q');
  questions.forEach(qEl => {
    qEl.addEventListener('click', () => {
      const aEl = qEl.nextElementSibling;
      const isOpening = !aEl.classList.contains('open');

      document.querySelectorAll('.respond .a').forEach(el => {
        el.classList.remove('open');
        el.style.display = 'none';
      });
      document.querySelectorAll('.respond .q').forEach(el => {
        el.classList.remove('open');
        const arrow = el.querySelector('.arrow');
        if (arrow) arrow.textContent = '▶';
      });

      if (isOpening) {
        aEl.classList.add('open');
        aEl.style.display = 'block';
        qEl.classList.add('open');
        const arrow = qEl.querySelector('.arrow');
        if (arrow) arrow.textContent = '▼';
      }
    });
  });

});
