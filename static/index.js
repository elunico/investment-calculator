
let principleElt = document.getElementById('principle');
let interestElt = document.getElementById('interest');
let contributionElt = document.getElementById('contribution');
let frequencyElt = document.getElementById('frequency');
let durationElt = document.getElementById('duration');

frequencyElt.selectedIndex = 2;

let fetching = false;

function didInput() {
  if (fetching) return;
  fetching = true;

  doSubmit();
}

function doSubmit() {
  try {
    let r = document.getElementById('result');

    let principle = principleElt.value;
    let interest = interestElt.value;
    let contribution = contributionElt.value;
    let frequency = frequencyElt.selectedOptions[0].value;
    let duration = durationElt.value;

    let data = {
      principle,
      interest,
      contribution,
      frequency,
      duration
    };

    fetch('/calculate', {
      headers: {
        "Content-Type": "application/json",
        "Content-Length": JSON.stringify(data).length
      },
      method: "POST",
      body: JSON.stringify(data)
    }).then(r => r.text()).then(text => {
      console.log(r, text);
      r.textContent = text;
    }).catch(err => {
      r.textContent = err;
    });
  } finally {
    fetching = false;
  }

}

