// export to ptcontrol

document.addEventListener("DOMContentLoaded", function () {
  // ========= 切換表格 =========
  const tabs = document.querySelectorAll('.tabs li');
  const tables = document.querySelectorAll('.table-container table');
  console.log("tabs:", tabs.length);
  console.log("tables:", tables.length);
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tables.forEach(table => table.classList.remove('open'));

      tab.classList.add('active');
      tables[i].classList.add('open');
    });
  });
  // ========= 移除message(擋到tags了) =========
  document.querySelectorAll('.message').forEach(msg => {
      msg.addEventListener("animationend", () => {
        msg.style.display = "none";
      });
  });
});