
let allNotes = [];
let editingNoteId = null;

// Initialize application
document.addEventListener("DOMContentLoaded", () => {
    loadNotes();

    document.getElementById("searchInput")
        .addEventListener("input", displayNotes);

    document.getElementById("todayDate").textContent =
        new Date().toLocaleDateString("en-IN", {
            day: "numeric",
            month: "long",
            year: "numeric"
        });
});


// Save note
async function saveNote() {
    const input = document.getElementById("noteInput");
    const message = document.getElementById("message");
    const button = document.getElementById("saveBtn");

    const content = input.value.trim();

    if (!content) {
        message.textContent = "Please write something first!";
        message.style.color = "#dc5555";
        return;
    }

    button.disabled = true;

    try {
        const response = await fetch("/api/notes", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Could not save note");
        }

        input.value = "";
        message.textContent = "Your note was saved successfully!";
        message.style.color = "#219653";

        await loadNotes();

    } catch (error) {
        message.textContent = error.message;
        message.style.color = "#dc5555";
    } finally {
        button.disabled = false;
    }
}


// Load notes from database
async function loadNotes() {
    const notesList = document.getElementById("notesList");

    try {
        const response = await fetch("/api/notes");

        if (!response.ok) {
            throw new Error("Unable to load notes");
        }

        allNotes = await response.json();

        document.getElementById("totalNotes").textContent =
            allNotes.length;

        displayNotes();

    } catch (error) {
        notesList.textContent = error.message;
    }
}


// Display notes
function displayNotes() {
    const notesList = document.getElementById("notesList");

    const search = document.getElementById("searchInput")
        .value.toLowerCase().trim();

    const filteredNotes = allNotes.filter(note =>
        note.content.toLowerCase().includes(search)
    );

    notesList.replaceChildren();

    if (filteredNotes.length === 0) {
        const empty = document.createElement("div");
        empty.className = "empty-state";

        empty.textContent = search
            ? "No notes match your search."
            : "✦ No notes yet. Create your first note above!";

        notesList.appendChild(empty);
        return;
    }

    filteredNotes.forEach(note => {
        const card = document.createElement("div");
        card.className = "note-card";

        const content = document.createElement("p");
        content.textContent = note.content;

        const date = document.createElement("small");
        date.textContent = "Created: " + note.created_at;

        const actions = document.createElement("div");
        actions.className = "note-actions";

        const editButton = document.createElement("button");
        editButton.className = "edit-btn";
        editButton.textContent = "✎ Edit";
        editButton.onclick = () =>
            openEditModal(note.id, note.content);

        const deleteButton = document.createElement("button");
        deleteButton.className = "delete-btn";
        deleteButton.textContent = "♲ Delete";
        deleteButton.onclick = () =>
            deleteNote(note.id);

        actions.append(editButton, deleteButton);
        card.append(content, date, actions);

        notesList.appendChild(card);
    });
}


// Open edit popup
function openEditModal(id, content) {
    editingNoteId = id;

    document.getElementById("editInput").value = content;

    document.getElementById("editModal")
        .classList.add("show");
}


// Close edit popup
function closeEditModal() {
    editingNoteId = null;

    document.getElementById("editModal")
        .classList.remove("show");
}


// Update note
async function updateNote() {
    const content = document.getElementById("editInput")
        .value.trim();

    if (!content) {
        alert("Note cannot be empty!");
        return;
    }

    try {
        const response = await fetch(
            `/api/notes/${editingNoteId}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ content })
            }
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Update failed");
        }

        closeEditModal();
        await loadNotes();

    } catch (error) {
        alert(error.message);
    }
}


// Delete note
async function deleteNote(id) {
    const confirmDelete = confirm(
        "Are you sure you want to delete this note?"
    );

    if (!confirmDelete) return;

    try {
        const response = await fetch(`/api/notes/${id}`, {
            method: "DELETE"
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Delete failed");
        }

        await loadNotes();

    } catch (error) {
        alert(error.message);
    }
}


// Close popup when clicking outside
document.getElementById("editModal")
    .addEventListener("click", event => {
        if (event.target.id === "editModal") {
            closeEditModal();
        }
    });
