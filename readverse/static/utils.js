/**
 * @param {String} html HTML representing a single element.
 * @param {Boolean} trim flag representing whether or not to trim input whitespace, defaults to true.
 * @return {Element}
 */
function fromHTML(html, trim = true) {
  // Process the HTML string.
  html = trim ? html : html.trim();

  // Then set up a new template element.
  const template = document.createElement("template");
  template.innerHTML = html;
  const result = template.content.children;

  // Then return either an HTMLElement or HTMLCollection,
  // based on whether the input HTML had one or more roots.
  if (result.length === 1) return result[0];
  return result;
}

/**
 * @template T
 * @param {T} callback
 * @param {number} wait Wait time in miliseconds
 * @return {T}
 */
function debounce(callback, wait) {
  let timeoutId = null;
  return (...args) => {
    window.clearTimeout(timeoutId);
    timeoutId = window.setTimeout(() => {
      callback.apply(null, args);
    }, wait);
  };
}
