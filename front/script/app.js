'use strict';

const ip = window.location.host;
const socket = io.connect(ip + ':5000');
const backend_IP = `http://${ip}:5000`;
const backend = backend_IP + '/api/v1';

const doSocket = function() {
  socket.emit('naarfrontend', function() {
    print('emit ontvangen');
  });
  socket.on('temp_terug', function(data) {
    const tempdiv = document.querySelector('.js-temp');
    const emoji = document.querySelector('.js-emoji');
    tempdiv.innerHTML = `<p>${data}</p>`;
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
};

const getTableData = function() {
  handleData(`${backend}/table`, verwerkDatatable, 'GET');
};

const verwerkDatatable = function(data) {
  console.log(data);
  const table = document.querySelector('.js-table');
  table.innerHTML = `<tr class="js-table-header">
  <td>Naam:</td>
  <td>Toevoegdatum:</td>
  <td>Vervaldatum:</td>
  <td>Aantal:</td>
  <td class="js-delete">Verwijderen:</td>
</tr>`;
  for (let object of data) {
    const amount = object.amount;
    const name = object.name;
    const addDate = object.date;
    const exDate = object.expirationDate;
    table.innerHTML += `<tr>
  <td class="js-name">${name}</td>
  <td>${addDate}</td>
  <td>${exDate}</td>
  <td>${amount}</td>
  <td class="js-delete js-listendelete"> <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M3 8v16h18v-16h-18zm5 12c0 .552-.448 1-1 1s-1-.448-1-1v-8c0-.552.448-1 1-1s1 .448 1 1v8zm5 0c0 .552-.448 1-1 1s-1-.448-1-1v-8c0-.552.448-1 1-1s1 .448 1 1v8zm5 0c0 .552-.448 1-1 1s-1-.448-1-1v-8c0-.552.448-1 1-1s1 .448 1 1v8zm4-15.375l-.409 1.958-19.591-4.099.409-1.958 5.528 1.099c.881.185 1.82-.742 2.004-1.625l5.204 1.086c-.184.882.307 2.107 1.189 2.291l5.666 1.248z"/></svg></td>
</tr>`;
  }
  listenToTrash();
};

const listenToTrash = function() {
  const trashButton = document.querySelector('.js-trash');
  trashButton.addEventListener('click', function() {
    const del = document.querySelectorAll('.js-delete');
    let i;
    for (i = 0; i < del.length; i++) {
      if (del[i].style.display == 'none') {
        del[i].style.display = 'block';
      } else {
        del[i].style.display = 'none';
      }
    }
  });
  listenToTrashes();
};

const listenToTrashes = function() {
  document
    .querySelector('.js-table')
    .addEventListener('click', function(event) {
      const delButton = event.target.closest('.js-listendelete');
      if (delButton && this.contains(delButton)) {
        const firstCell = delButton.closest('tr').querySelector('td');
        if (firstCell) {
          console.log(firstCell.innerHTML);
          const data = firstCell.innerHTML;
          const body = `{"htmlvalue" : "${data}"}`;
          handleData(backend + '/table', next, 'POST', body);
        }
      }
    });
};

const next = function() {
  console.log('done');
  location.reload();
};

document.addEventListener('DOMContentLoaded', function() {
  console.info('DOM geladen');
  doSocket();
  getTableData();
});
