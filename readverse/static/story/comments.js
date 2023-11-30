import {
  createSignal,
  createResource,
  Suspense,
  For,
} from "https://cdn.skypack.dev/solid-js";
import { render } from "https://cdn.skypack.dev/solid-js/web";
import html from "https://cdn.skypack.dev/solid-js/html";

const options = {
  year: "numeric",
  month: "numeric",
  day: "numeric",
  hour: "numeric",
  minute: "numeric",
  second: "numeric",
};

const formatter = new Intl.DateTimeFormat("en-US", options);
const storyId = window.location.pathname.trimEnd("/").split("/").slice(-1)[0];

/**
 * @typedef {Object} Comment
 * @property {string} content
 * @property {string} timestamp
 * @property {string} username
 */

/**
 * @template T
 * @typedef {Object} ServerResponse
 * @property {string} message
 * @property {T} data
 */

/**
 * @returns {Promise<ServerResponse<Comment>>}
 */
const fetchComments = async () => {
  return (await fetch(`/story/${storyId}/comments`)).json();
};

const Comment = (props) => {
  /** @type {Comment} */
  const comment = props.comment;

  return html`<div
    class="flex flex-col gap-2 p-4 rounded-md border border-primary"
  >
    <div class="flex flex-col md:flex-row justify-between md:items-center">
      <strong class="font-bold">${comment.username}</strong>
      <time class="text-sm text-gray-500" datetime=${comment.timestamp}
        >${formatter.format(new Date(comment.timestamp))}</time
      >
    </div>
    <p>${comment.content}</p>
  </div>`;
};

const CommentSection = () => {
  const [content, setContent] = createSignal("");
  const [comments, { refetch }] = createResource(fetchComments);
  const emptyComments = { data: [] };

  async function postComment() {
    await fetch(`/story/${storyId}/comment`, {
      method: "POST",
      body: JSON.stringify({ content: content() }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    alert("Successfully commented!");
    refetch();
  }

  return html`<div class="flex flex-col gap-4">
    <textarea
      class="textarea textarea-bordered w-full"
      onChange=${(e) => setContent(e.currentTarget.value)}
    ></textarea>
    <button
      class="btn btn-primary w-fit ml-auto"
      onClick=${() => postComment()}
    >
      Comment
    </button>

    <${For} each=${() => (comments() || emptyComments).data}>
      ${(comment) => html`<${Comment} comment=${comment} />`}
    <//>
  </div>`;
};

render(CommentSection, document.querySelector("#comments"));
