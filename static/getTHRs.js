const mainDiv = document.querySelector('.main');

fetch('/api/getthreads')
  .then(response => response.json())
  .then(data => {
    data.forEach(thread => {
        const threadBlock = document.createElement('div');
        threadBlock.classList.add('thread-block');

        const nameElement = document.createElement('a');
        nameElement.href = `/thread/${thread.name}`;
        nameElement.textContent = `${thread.name}`;
        threadBlock.appendChild(nameElement);

        const dateElement = document.createElement('p');
        dateElement.textContent = `Date: ${thread.date}`;
        threadBlock.appendChild(dateElement);

        mainDiv.appendChild(threadBlock);
    });
  })
  .catch(error => {
    // Handle any errors that occurred during the request
    console.error('Error:', error);
  });


