// your JavaScript file
const container = document.querySelector("#container");

const content = document.createElement("div");
content.classList.add("content");
content.textContent = "This is the glorious text-content!";

container.appendChild(content);

// adding red p
const content2 = document.createElement('p');
content2.textContent = 'hey im red!';
content2.style.color = 'red';
container.appendChild(content2);

// adding blue h3
const content3 = document.createElement('h3');
content3.textContent = 'im a blue h3!';
content3.style.color = 'blue';
container.appendChild(content3);

// adding div with childs
const content4 = document.createElement('div');
content4.style.backgroundColor = 'pink';
content4.style.border = 'black';

const content41 = document.createElement('h1');
content41.textContent = 'im in a div';
content4.appendChild(content41);

const content42 = document.createElement('p');
content42.textContent = 'me too';
content4.appendChild(content42);

container.appendChild(content4);

// event listeners