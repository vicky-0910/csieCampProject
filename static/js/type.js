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
    }
  }

  typeLetter();
});
