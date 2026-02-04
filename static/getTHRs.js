const mainDiv = document.querySelector('.main');
// Get the full URL
const currentUrl = window.location.pathname;
let current_page = 1
console.log('Current URL:', currentUrl);

if(currentUrl.split('/').indexOf('threads')+1){
  current_page = currentUrl.split('/')[currentUrl.split('/').indexOf('threads')+1];
} else {
  current_page = 1;
}

console.log(current_page);

fetch('/api/getthreads')
  .then(response => response.json())
  .then(data => {
    console.log(data);
    data.forEach(thread => {
        const threadBlock = document.createElement('div');
        threadBlock.classList.add('thread-block');

        const nameElement = document.createElement('a');
        nameElement.href = `/thread/${thread.name}/1`;
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


