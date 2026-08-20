# Music Bingo

A Python-based music bingo card generator that creates printable bingo cards from music artists and tracks. The project can pull music data from APIs, generate randomized bingo cards, and produce printable PDF sheets.

## Features

* Generate randomized music bingo cards
* Use music tracks as bingo spaces
* Generate printable PDF bingo cards
* Retrieve music data through APIs
* Create Spotify playlists from selected music (where supported)
* Docker support for running the application in a consistent environment
* Flask-based web interface/API

## Tech Stack

* **Python**
* **Flask**
* **Pandas**
* **Spotipy / Spotify Web API**
* **Last.fm API**
* **Docker**
* **Postgresql**
* **Javascript**
* **LibreOffice** for PDF generation/conversion

## Setup

Clone the repository and create a Python virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
.\venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file containing the required API credentials. **Do not commit this file or any Spotify authentication cache/token files to Git.**

## Running the Application

With the virtual environment activated:

```bash
python app.py
```

The Flask application will start locally. Open the address shown in the terminal in your browser.

## Docker

The project also includes Docker support. Build the image with:

```bash
docker build -t music-bingo .
```

Then run the container according to the application's configured ports and environment variables.

## API Endpoints

The Flask application includes endpoints for music data and playlist functionality, including:

* `/api/recent_artists`
* `/api/artists`
* `/api/artists/<artist>`
* `/api/top-tags`
* `/api/tag-songs/<tag>`
* `/api/create_playlist`

## Security

API credentials and authentication tokens should be stored in environment variables or local configuration files and **never committed to the repository**.

The Spotify `.cache` authentication file is also excluded from version control.

## Project Status

This is project is being actively developed, with additional features expected in upcoming versions. 
