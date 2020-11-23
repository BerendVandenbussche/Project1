'use strict';

const ip = window.location.host;
const socket = io.connect(ip + ':5000');

const init = function() {
  laadData();
};

const laadData = function() {
  fetch(`http://${ip}:5000/api/v1/temperature_history`)
    .then(function(response) {
      if (!response.ok) {
        throw Error(`Probleem bij de fetch(). Status Code: ${response.status}`);
      } else {
        console.info('Er is een response teruggekomen van de server');
        return response.json();
      }
    })
    .then(function(jsonObject) {
      console.info('json object is aangemaakt');
      console.info('verwerken data');
      verwerkData(jsonObject);
    })
    .catch(function(error) {
      console.error(`fout bij verwerken json ${error}`);
    });
};

const verwerkData = function(jsonObject) {
  console.log(jsonObject);
  let arrLabels = [];
  let arrValue = [];
  for (let object of jsonObject) {
    let label = object.time;
    let value = object.temperature;
    arrLabels.push(label);
    arrValue.push(value);
  }
  displayChart(arrLabels, arrValue);
};

const displayChart = function(label, value) {
  var ctx = document.getElementById('myChart');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: label,
      datasets: [
        {
          label: 'Temperatuur in de koelkast',
          data: value,
          borderColor: '#5184BA',
          backgroundColor: 'rgba(255,255,255,0)'
        }
      ],
      borderColor: 'rgba(241, 169, 160, 1)',
      borderWidth: 1
    }
  });
};

socket.emit('naarfrontend', function() {
  print('emit ontvangen');
});
socket.on('temp_terug', function(data) {
  const tempdiv = document.querySelector('.js-temp');
  const emoji = document.querySelector('.js-emoji');
  tempdiv.innerHTML = `<p>${data} &deg;C</p>`;
  console.log('temp_terug');
  if (data >= 11) {
    tempdiv.innerHTML = `<span class="c-temperature">${data} &deg;C<span/><span class="c-temp-disc">De temperatuur in de koelkast is te warm!</span>`;
    emoji.innerHTML = `<img src="img/fire.png" alt="vuur emoji">`;
  } else if (data >= 7) {
    tempdiv.innerHTML = `<span class="c-temperature">${data} &deg;C<span/><span class="c-temp-disc">De temperatuur in de koelkast wordt te warm!</span>`;
    emoji.innerHTML = `<img src="img/sun-behind-cloud.png" alt="zon achter wolk emoji">`;
  } else if (data >= 0) {
    tempdiv.innerHTML = `<span class="c-temperature">${data} &deg;C<span/><span class="c-temp-disc">De temperatuur in de koelkast is perfect! </span>`;
    emoji.innerHTML = `<img src="img/snowflake.png" alt="sneeuwvlok emoji">`;
  }
});

document.addEventListener('DOMContentLoaded', function() {
  console.info('DOM geladen');
  init();
});
