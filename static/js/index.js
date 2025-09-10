// export to index

document.addEventListener("DOMContentLoaded", function () {

  // ========= 打字動畫 =========
  const type = document.getElementById("typeTarget");
  const text = type.innerText.trim();
  const main = document.getElementById("main");
  type.innerHTML = "";

  let i = 0;

  function typeLetter() {
    if (i < text.length) {
      if (text[i] === ".") {
        type.innerHTML += "<br>";
      } else {
        type.innerHTML += text[i];
      }
      i++
      setTimeout(typeLetter,60);
    } else {
      const arrow = document.createElement("span");
      arrow.id = "arrow";
      arrow.textContent = "▼";
      arrow.classList.add("blink");
      type.appendChild(arrow);

      main.classList.remove("hidden-before-type");
      main.classList.add("fade-in");
      setTimeout(() => {
      arrow.classList.remove("blink");
    }, 1500);

    }
  }

  typeLetter();

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
