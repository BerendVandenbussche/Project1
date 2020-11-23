'use strict';
const ip = window.location.host;
const backIp = `http://${ip}:5000/api/v1/unit`;

const init = function() {
  const radiovalues = document.forms['settings'].elements['eenheid'];
  for (let radiovalue in radiovalues) {
    radiovalues[radiovalue].onclick = function() {
      console.log(this.value);
      sendUnitToBack(this.value);
    };
  }
};

const getUnit = function() {
  fetch(backIp)
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
      setUnit(jsonObject);
    })
    .catch(function(error) {
      console.error(`fout bij verwerken json ${error}`);
    });
};

const setUnit = function(data) {
  console.log(data);
  const str = JSON.stringify(data);
  console.log(str);
  const form = document.querySelector('.js-input');
  if (data == 'C') {
    form.innerhtml = `<h5>Temperatuur:</h5>
    <p class="c-formtitle">Eenheid:</p>
        <input type="radio" name="eenheid" value="°C" checked>°C
        <input type="radio" name="eenheid" value="°F"> °F<br>
        <p class="c-formtitle">Signaal bij te lang open:</p>
        <label class="switch">
                <input type="checkbox">
                <span class="slider round"></span>
              </label>`;
  } else if (data == 'F') {
    form.innerhtml = `<h5>Temperatuur:</h5>
    <p class="c-formtitle">Eenheid:</p>
        <input type="radio" name="eenheid" value="°C">°C
        <input type="radio" name="eenheid" value="°F" checked> °F<br>
        <p class="c-formtitle">Signaal bij te lang open:</p>
        <label class="switch">
                <input type="checkbox">
                <span class="slider round"></span>
              </label>`;
  }
  init();
};

const handleData = function(url, callback, method = 'GET', body = null) {
  fetch(url, {
    method: method,
    body: body,
    headers: { 'content-type': 'application/json' }
  })
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
      callback(jsonObject);
    })
    .catch(function(error) {
      console.error(`fout bij verwerken json ${error}`);
    });
};

const sendUnitToBack = function(unit) {
  handleData(backIp, blabla, 'POST', unit);
};

const blabla = function() {
  console.log('lol');
};

document.addEventListener('DOMContentLoaded', function() {
  console.info('DOM geladen');
  getUnit();
});
