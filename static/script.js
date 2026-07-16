document.addEventListener("DOMContentLoaded", loadArtists);

document
  .getElementById("search-button")
  .addEventListener("click", searchArtist);

document.getElementById("clear-button").addEventListener("click", clearForm);

async function loadArtists() {
  const response = await fetch("/api/artists");
  const artists = await response.json();

  const container = document.getElementById("artist-buttons");
  artists.forEach((artist) => {
    const button = document.createElement("button");
    button.textContent = artist;
    container.appendChild(button);
    button.addEventListener("click", () => {
      loadSongs(artist);
    });
  });
}

async function loadSongs(artist) {
  const response = await fetch("/api/artists/" + encodeURIComponent(artist));
  const songs = await response.json();
  document.getElementById("songs").value = songs.join("\n");
  document.getElementById("title").value = artist;
}

async function searchArtist() {
  const artist = document.getElementById("artist-search").value;
  if (artist) {
    loadSongs(artist);
  }
}

async function clearForm() {
  document.getElementById("songs").value = "";
  document.getElementById("title").value = "";
}
