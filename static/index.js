
let fetching = false;
let principleElt = document.getElementById('principle');
let interestElt = document.getElementById('interest');
let contributionElt = document.getElementById('contribution');
let frequencyElt = document.getElementById('frequency');
let durationElt = document.getElementById('duration');
let r = document.getElementById('result');
let pr = document.getElementById('presult');
let cr = document.getElementById('cresult');
let ir = document.getElementById('iresult');

frequencyElt.selectedIndex = 2;

function didInput() {
  if (fetching) {
    return;
  };
  fetching = true;

  doSubmit();
}

function doSubmit() {
  try {

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
    }).then(r => r.json())
      .then(json => {
        if (json.message) {
          r.textContent = json.message;
          return;
        }

        let n = Intl.NumberFormat('en-US', {
          'currency': 'USD',
          'maximumFractionDigits': 2,
          'minimumFractionDigits': 2,
          'currencyDisplay': 'symbol',
          'currencySign': 'standard'
        });

        r.textContent = `$${n.format(json.total)}`;
        pr.textContent = `$${n.format(json.principle)}`;
        cr.textContent = `$${n.format(json.contributions)}`;
        ir.textContent = `$${n.format(json.interest)}`;

      })
      .catch(err => {
        console.log(err);
        r.textContent = err.message;
      });
  } finally {
    fetching = false;
  }
}
