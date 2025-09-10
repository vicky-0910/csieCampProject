// export to ptcontrol

document.addEventListener("DOMContentLoaded", function () {
  // ========= Bingo即時計分 =========
  const tbingo = document.querySelector("#bingo tbody");
  const bingono1 = 75000;
  const bStep = 5000;

  function bingoScores() {
    let teams = [];
    const rows = tbingo.querySelectorAll("tr");

    rows.forEach((row, idx) => {
      const itemInput = row.cells[1].querySelector("input");
      const lineInput = row.cells[2].querySelector("input");

      let items = parseInt(itemInput.value) || 0;
      let lines = parseInt(lineInput.value) || 0;
      let score = items * 3 + lines * 10;

      teams.push({ row, score });
    });

    teams.sort((a, b) => b.score - a.score);

    let rank = 1;
    let prescore = teams[0].score;
    teams.forEach((team, index) => {
      if (team.score < prescore){
        rank+=1;
        prescore = team.score;
      }
      let pts = bingono1 - ((rank-1) * bStep);

      team.row.cells[3].innerText = team.score;
      team.row.cells[4].innerText = `${rank}`;
      team.row.cells[5].innerText = `${pts} pt`;
    });
  }

  tbingo.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", bingoScores);
  });

  // ========= 積彈高計分 =========
  const tbank = document.querySelector("#casinobank tbody tr");
  const tend = document.querySelector("#casinoend tbody");
  const cstep = 500;

  const teamSelect = document.querySelector("select[name='teamid']");
  const pointsCell = document.querySelector("#casinobank tbody tr td:nth-child(2)");

  teamSelect.addEventListener("change", function() {
      const selectedOption = this.selectedOptions[0];
      pointsCell.textContent = selectedOption.dataset.points + " pt";
  });

  function bank() {
    const currentPoint = tbank.cells[1].innerText.replace(" pt", "");
    const cashInput = tbank.querySelector("input");
    let restpt = parseInt(currentPoint) - (parseInt(cashInput.value) || 0) * cstep;
    tbank.cells[3].innerText = `${restpt} pt`;
  }
  tbank.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", bank);
  }); 

  function settle() {
    const rows = tend.querySelectorAll("tr");
    rows.forEach((row, idx) => {
      const cashInput = row.querySelector("input");
      const savingText = row.cells[1].innerText.replace(" pt", "");
      const saving = parseInt(savingText) || 0;
      const cash = parseInt(cashInput.value) || 0;
      const pts = Math.floor(saving * 1.1 + cash * cstep);
      row.cells[3].innerText = `${pts} pt`;
    });
  }
  tend.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", settle);
  });
  settle();
});