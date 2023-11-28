/// <reference path="../utils.js"/>

const genreContainer = document.querySelector("#genrecontainer");
document.querySelector("#addGenreBtn").addEventListener("click", (e) => {
  e.preventDefault();
  const node = fromHTML(`<div class="flex flex-row gap-2">
    <button class="btn btn-error text-xl">&times;</button>
    <input class="input input-bordered w-full" type="text" name="genres" />
  </div>`);

  genreContainer.append(node);
  node.querySelector("button").addEventListener("click", (e) => {
    e.preventDefault();
    node.remove();
  });
});

const previewContainer = document.querySelector("#preview");

/** @type {HTMLInputElement} */
const contentInput = document.querySelector("#content");
contentInput.addEventListener(
  "change",
  debounce((e) => {
    previewContainer.innerHTML = DOMPurify.sanitize(
      marked.parse(contentInput.value)
    );
  }, 1000)
);
