const storyId = window.location.pathname.trimEnd("/").split("/").slice(-1)[0];

const removeBtn = document.querySelector("#removebtn")
if (removeBtn) removeBtn.addEventListener("click", async (e) => {
    e.preventDefault();
    await fetch(`/story/${storyId}/delete`, {
        method: "DELETE"
    })

    alert("Successfully removed!")
    window.location = "/"
})
