let currentSongs = [];

document.addEventListener("DOMContentLoaded", () => {
  loadArtists();
  loadUserArtists();
  loadTags();
});

document
  .getElementById("search-button")
  .addEventListener("click", searchArtist);

document
  .getElementById("tag-search-button")
  .addEventListener("click", searchTag);

document
  .getElementById("generate-playlist")
  .addEventListener("click", createSpotifyPlaylist);

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

async function loadTags() {
  const response = await fetch("/api/top-tags");
  const tags = await response.json();

  const container = document.getElementById("tag-buttons");
  tags.forEach((tag) => {
    const button = document.createElement("button");
    button.textContent = tag.name;
    container.appendChild(button);
    button.addEventListener("click", () => {
      loadSongsByTag(tag.name);
    });
  });
}

async function loadSongs(artist) {
  currentSongs = [];
  const response = await fetch("/api/artists/" + encodeURIComponent(artist));
  currentSongs = await response.json();
  document.getElementById("songs").value = currentSongs
    .map((song) => `${song.name}`)
    .join("\n");
  document.getElementById("title").value = artist;
}

async function loadSongsByTag(tag) {
  currentSongs = [];
  const response = await fetch("/api/tag-songs/" + encodeURIComponent(tag));
  currentSongs = await response.json();
  document.getElementById("songs").value = currentSongs
    .map((song) => `${song.name}`)
    .join("\n");
  document.getElementById("title").value = tag;
}

async function searchArtist() {
  const artist = document.getElementById("artist-search").value;
  if (artist) {
    loadSongs(artist);
  }
}

async function searchTag() {
  const tag = document.getElementById("tag-search").value;
  if (tag) {
    loadSongsByTag(tag);
  }
}

async function clearForm() {
  document.getElementById("songs").value = "";
  document.getElementById("title").value = "";
}

async function loadUserArtists() {
  console.log("loading user artists...");
  const response = await fetch("/api/recent_artists");
  const containerInit = document.getElementById("recent-artist-buttons");
  containerInit.innerHTML = "";

  if (response.status === 401) {
    const container = document.getElementById("recent-artist-buttons");
    const button = document.createElement("button");
    button.textContent = "Connect to Spotify!";
    container.appendChild(button);
    button.addEventListener("click", () => {
      window.location.href = "/spotify/login";
    });
    return;
  }
  const data = await response.json();

  const container = document.getElementById("recent-artist-buttons");
  data.artists.forEach((artist) => {
    const button = document.createElement("button");
    button.textContent = artist;
    container.appendChild(button);
    button.addEventListener("click", () => {
      loadSongs(artist);
    });
  });
}

async function createSpotifyPlaylist() {
  const title = document.getElementById("title").value;

  const response = await fetch("/api/create_playlist", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title: title,
      songs: currentSongs,
    }),
  });

  const result = await response.json();

  console.log(result);
}

document.querySelectorAll(".tab-button").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tab-button").forEach((tab) => {
      tab.classList.remove("active");
    });

    document.querySelectorAll(".tab-content").forEach((content) => {
      content.classList.remove("active");
    });

    button.classList.add("active");

    document.getElementById(button.dataset.tab).classList.add("active");
  });
});
