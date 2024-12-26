const mainDiv = document.querySelector('.main');
const nameBlock = document.querySelector('.username').textContent

setTimeout(function() {
    console.log('Delayed execution');
  }, 1000);



thrname = document.querySelector('.threadname').textContent


fetch('/api/getthread/'+ thrname)
  .then(response => response.json())
  .then(data => {
    console.log(data)
    // Process the data received from the server
    const messagesDiv = document.createElement('div');
    messagesDiv.classList.add('messages');
    mainDiv.appendChild(messagesDiv);

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
          const HideShowButt = document.createElement('button');
          HideShowButt.id = message.media_filename.split(".").shift()+'_BUTT';
          HideShowButt.textContent = 'Показать изображение'
          HideShowButt.onclick = function() {
            ShowHide(this);
          };
          mediaElement.appendChild(HideShowButt);

          const imgElement = document.createElement('img');
          imgElement.id = message.media_filename.split(".").shift();
          imgElement.src = `/static/media/${message.media_filename}`;
          imgElement.alt = '';
          imgElement.style.cssText = 'display:none;'
          imgElement.width = 250;
          imgElement.loading = 'lazy';
          imgElement.onclick = function() {
            makebigger(this);
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
  })
  .catch(error => {
    // Handle any errors that occurred during the request
    console.error('Error:', error);
  })
},);







show = false;





function ShowHide(button){
  image = document.querySelector(`#${button.id.split("_").shift()}`)
  console.log(`${button.id.split("_").shift()}`)
  show = !show
  if (show) {
        image.style.cssText = 'display:block;';
        button.textContent = 'Скрыть';
    } else {
        image.style.cssText = 'display:none;';
        button.textContent = 'Показать изображение';
    }
  };
