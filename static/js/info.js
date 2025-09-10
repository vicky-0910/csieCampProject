// export to all htmlfiles

document.addEventListener("DOMContentLoaded", function () {

  // ========= 展開導覽列 =========
  const menuBtn = document.getElementById('menuToggle');
  const menu = document.getElementById('dropdownMenu');
  const icon = document.getElementById('menuIcon');

  let isOpen = false;

  menuBtn.addEventListener('click', function () {
    isOpen = !isOpen;
    menu.classList.toggle('open', isOpen);
    icon.src = isOpen ? iconOpen : iconClose;
  });

});
