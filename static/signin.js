let namestr = document.querySelector('.namesbl').value;

let names = namestr.split(',');

let warning = document.querySelector('.namecheck');

let name;

function check(element){
    let tr;
    let name;
    name = element.value;
    if (names.includes(name)) {
        tr = 'занято'
    } else {
        tr = 'свободно'
    }
    warning.textContent = 'Имя' + ' ' + name + ' ' + tr;
}





/**dddddddddddddddddddddddddddddd */
/*
let name = document.querySelector(".name");
let password = document.querySelector(".password");

const url = '/data';
const xhr = new XMLHttpRequest();

const formData = new FormData();


function send(){
	formData.append('name', name.value);
	formData.append('message', password.value);
	xhr.open('POST', url, true);
	xhr.send(formData);
}

*/

