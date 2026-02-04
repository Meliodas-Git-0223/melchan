const mainDiv = document.querySelector('.main');
const nameBlock = document.querySelector('.username').textContent;
const threadName = document.querySelector('.threadname').textContent;


setTimeout(function() {
  const nextPage_prevPage = document.createElement('div');
  nextPage_prevPage.classList.add('message-block');
  nextPage_prevPage.setAttribute('id', 'next-page_prev-page');
  mainDiv.appendChild(nextPage_prevPage);
  
  const nextPage = document.createElement('a');
  nextPage.classList.add('next-page');
  nextPage.textContent = "   >>>Следующая>>>";
  nextPage.href = `/thread/${threadName}/${parseInt(page)+1}`;

  const prevPage = document.createElement('a');
  prevPage.classList.add('next-page');
  prevPage.textContent = "<<<Предыдущая<<<   ";
  prevPage.href = `/thread/${threadName}/${parseInt(page)-1}`;
  
  nextPage_prevPage.appendChild(prevPage);
  nextPage_prevPage.appendChild(nextPage);
  }, 1000);


thrname = document.querySelector('.threadname').textContent

let page = String(document.location).split('/')[String(document.location).split('/').length-1];
console.log(`page ${String(document.location).split('/')[String(document.location).split('/').length-1]}`)

const messagesDiv = document.createElement('div');
    messagesDiv.classList.add('messages');
    mainDiv.appendChild(messagesDiv);

fetch(`/api/getthread/${thrname}/${page}`)
  .then(response => response.json())
  .then(data => {
    console.log(data)
    // Process the data received from the server
    data.forEach(message => {
      const messageDiv = document.createElement('div');
      messageDiv.classList.add('message-block');
      messageDiv.setAttribute('id', message.id);
      console.log(message.name);
      console.log(nameBlock);
      if (message.name == nameBlock){
        messageDiv.classList.add('my-message')
      } else {
        messageDiv.classList.add('not-my-message')
      }
      messagesDiv.appendChild(messageDiv);

      const nameElement = document.createElement('a');
      nameElement.href = `/user/${message.name}`;
      nameElement.textContent = `${message.name}`;
      messageDiv.appendChild(nameElement);

      if (message.text != null){
        const messageText = document.createElement('p');
        messageText.classList.add('message-text');
        messageText.textContent = `${message.text}`;
        messageDiv.appendChild(messageText);
      }

      if (message.media) {
        const mediaElement = document.createElement('div');
        mediaElement.classList.add('media');
        messageDiv.appendChild(mediaElement);

        if (message.media === 'image') {
          const imgElement = document.createElement('img');
          imgElement.id = message.thumbnail;
          imgElement.src = `/static/media/thumbnails/${message.thumbnail}`;
          imgElement.style.maxWidth = '85%';
          imgElement.onclick = function() {
            const imgElementf = document.createElement('img');
            imgElementf.id = message.media_filename;
            imgElementf.src = `/static/media/full/${message.media_filename}`;
            imgElementf.classList.add('fullImage')
            mediaElement.removeChild(imgElement);
            mediaElement.appendChild(imgElementf);
          };
          mediaElement.appendChild(imgElement);
        } else if (message.media === 'audio') {
          const audioElement = document.createElement('audio');
          audioElement.controls = true;
          audioElement.loading = 'lazy';
          audioElement.src = `/static/media/${message.media_filename}`;
          mediaElement.appendChild(audioElement);
        } else if (message.media === 'video') {
          const videoElement = document.createElement('video');
          videoElement.controls = true;
          videoElement.loading = 'lazy';
          videoElement.src = `/static/media/${message.media_filename}`;
          videoElement.type = `video/${message.media_filename.split('.').pop()}`;
          mediaElement.appendChild(videoElement);
        }
      }

      const dateElement = document.createElement('p');
      dateElement.classList.add('message-date');
      dateElement.textContent = `Date: ${message.date}`;
      messageDiv.appendChild(dateElement);

      if (message.name == nameBlock){
        const deleteButton = document.createElement('button');
        deleteButton.classList.add('delete_button');
        deleteButton.addEventListener('click', () => deleteMessage(threadName,message.id));
        deleteButton.textContent = `delete message`;
        messageDiv.appendChild(deleteButton);
      }


  })

  
  .catch(error => {
    // Handle any errors that occurred during the request
    console.error('Error:', error);
  })
},);


function deleteMessage(threadName,message){
  fetch(`/deletemypost/${threadName}/${message}`)
  console.log(`${threadName}/${message}`)
}