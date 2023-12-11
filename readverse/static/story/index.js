const storyId = window.location.pathname.trimEnd("/").split("/").slice(-1)[0];

const removeBtn = document.querySelector("#removebtn");
if (removeBtn)
  removeBtn.addEventListener("click", async (e) => {
    try {
      e.preventDefault();
      const res = await fetch(`/story/${storyId}/delete`, {
        method: "DELETE",
      });
      if (!res.ok) {
        throw Error(res.statusText);
      }

      alert("Successfully removed!");
      window.location = "/";
    } catch (e) {
      alert(`Failed to remove story: ${e.message}`);
    }
  });
