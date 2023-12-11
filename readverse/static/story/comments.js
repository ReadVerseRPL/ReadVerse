import {
  createSignal,
  createResource,
  Show,
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
const commentDiv = document.querySelector("#comments");
const isAdmin = commentDiv.dataset.admin == "True";
const currentUsername = commentDiv.dataset.currentUsername;

/**
 * @typedef {Object} Comment
 * @property {string} id
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
  const res = await fetch(`/story/${storyId}/comments`);
  if (!res.ok) {
    throw Error(res.statusText);
  }
  return res.json();
};

const Comment = (props) => {
  /** @type {Comment} */
  const comment = props.comment;

  async function deleteComment() {
    try {
      const res = await fetch(
        `/story/${storyId}/comment/${comment.id}/delete`,
        {
          method: "DELETE",
        }
      );
      if (!res.ok) {
        throw Error(res.statusText);
      }

      alert("Successfully deleted!");
      props.refetch();
    } catch (e) {
      alert(`Failed to delete comment: ${e.message}`);
    }
  }

  return html`<div
    class="flex flex-col gap-2 p-4 rounded-md border border-primary"
  >
    <div class="flex flex-col md:flex-row justify-between md:items-center">
      <a
        class="font-bold link link-hover hover:text-gray-300"
        href=${`/profile/${comment.username}`}
        >${comment.username}</a
      >
      <div>
        ${(comment.username == currentUsername || isAdmin) &&
        html`<a
          class="mr-4 hover:underline hover:text-gray-300 hover:cursor-pointer"
          onClick=${() => deleteComment()}
        >
          Delete
        </a>`}
        <time class="text-sm text-gray-500" datetime=${comment.timestamp}
          >${formatter.format(new Date(comment.timestamp))}</time
        >
      </div>
    </div>
    <p>${comment.content}</p>
  </div>`;
};

const CommentSection = () => {
  const [content, setContent] = createSignal("");
  const [comments, { refetch }] = createResource(fetchComments);
  const emptyComments = { data: [] };

  async function postComment() {
    try {
      const res = await fetch(`/story/${storyId}/comment`, {
        method: "POST",
        body: JSON.stringify({ content: content() }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      if (!res.ok) {
        throw Error(res.statusText);
      }

      alert("Successfully commented!");
      refetch();
    } catch (e) {
      alert(`Failed to comment: ${e.message}`);
    }
  }

  return html`<div class="flex flex-col gap-4">
    ${!isAdmin &&
    currentUsername != "" &&
    html`<>
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
    </>`}

    <${For}
      each=${() => (comments() || emptyComments).data}
      fallback=${() => html`<p>No comments</p>`}
    >
      ${(comment) =>
        html`<${Comment} comment=${comment} refetch=${() => refetch} />`}
    <//>
  </div>`;
};

render(CommentSection, commentDiv);
