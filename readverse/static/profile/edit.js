/// <reference path="../utils.js"/>

const previewContainer = document.querySelector("#preview");

/** @type {HTMLInputElement} */
const contentInput = document.querySelector("#description");
contentInput.addEventListener(
  "change",
  debounce((e) => {
    previewContainer.innerHTML = DOMPurify.sanitize(
      marked.parse(contentInput.value)
    );
  }, 1000)
);

