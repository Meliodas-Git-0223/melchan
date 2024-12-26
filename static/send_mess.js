
/*
let message = document.querySelector(".message");

const url = '/newmessage';
const xhr = new XMLHttpRequest();

const formData = new FormData();


function send(){
	formData.append('message', message.value);
	xhr.open('POST', url, true);
	xhr.send(formData);
}
*/


function send(){
        let message = document.querySelector(".message-input");
        let name = document.querySelector('.username').textContent;
        let file = document.querySelector('#file');
        let threadname = document.querySelector('.threadname').textContent
        let emptyFile = document.createElement('input');
        emptyFile.type = 'file';

        const url = '/newmessage';
        const xhr = new XMLHttpRequest();
        const formData = new FormData();

	    formData.append('message', message.value);
        formData.append('name', name);
        if(file.files[0] != undefined){
            formData.append('file', file.files[0]); 
        }
        formData.append('tfile',(file.files[0] != undefined))
        formData.append('threadname', threadname);

	    xhr.open('POST', url, true);
	    xhr.send(formData);

        
        message.value = '';
        file.files = emptyFile.files;
    }


    document.addEventListener('DOMContentLoaded', function() {
    // Функция для имитации клика по кнопке
    function triggerButtonClick(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Предотвращаем стандартное поведение Enter
            document.getElementById('send').click(); // Имитируем клик по кнопке
        }
    }

    // Добавляем обработчик события keydown к телу документа
    document.addEventListener('keydown', triggerButtonClick);
    });
