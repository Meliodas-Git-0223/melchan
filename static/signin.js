let namestr = document.querySelector('.namesbl').value;

let names = namestr.split(',');

let warning = document.querySelector('.namecheck');

let name;

let button = document.querySelector('.submitbutt')

function check(element){
    let status;
    let name;
    name = element.value;

    if (name.length < 4){
        warning.textContent = 'Никнейм должен быть не короче 4 символов';
        button.disabled = true;

    }else if (name.length > 24){
        warning.textContent = 'Никнейм должен быть не длиннее 24 символов';
        button.disabled = true;
    } else{

        fetch('/api/checkname/' + name)
            .then(response => response.json())
            .then(data => {
                // Process the data received from the server
                if (data == 1) {
                    status = 'занято'
                    button.disabled = true;
                } else {
                    status = 'свободно'
                    button.disabled = false;
                }
                warning.textContent = 'Имя' + ' ' + name + ' ' + status;
                console.log(data);
            })
            .catch(error => {
                // Handle any errors that occurred during the request
                console.error('Error:', error);
            });
    }
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

