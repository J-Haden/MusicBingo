from flask import Flask, render_template, request, send_file, jsonify, redirect, session
from src.bingo import create_bingo_card
from pathlib import Path
from src.excel import create_excel_card
from src.pdf import convert_excel_to_pdf, merge_pdfs
from src.cleanup import clear_folder
from src.lastfm import get_top_artists, get_top_tracks, get_tag_tracks, get_top_tags
from src.spotify import get_user_recent_artists, create_spotify_playlist, oauth, get_spotify
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    
    title=request.form['title']
    songs = request.form['songs']
    number_of_sheets = int(request.form['number_of_sheets'])
    
    song_list = [song.strip() for song in songs.splitlines() if song.strip()]
    
    print('songs received:', len(song_list))
    
    
    template = Path('templates/bingo_template.xlsx')
    temp_folder = Path('temp')
    
    temp_folder.mkdir(exist_ok=True)
    clear_folder(temp_folder)
    clear_folder(Path('output'))
    
    for i in range(number_of_sheets):
        card = create_bingo_card(song_list)
        
        output = temp_folder / f'{title}_{i+1}.xlsx'
        
        create_excel_card(card, title, template, output)
    
    pdf_files = []
    
    for excel_file in temp_folder.glob('*.xlsx'):
        pdf_file = convert_excel_to_pdf(excel_file, temp_folder)
        pdf_files.append(pdf_file)
    
    final_pdf = Path(f'output/{title}music_bingo.pdf')
    merge_pdfs(pdf_files, final_pdf) 
    
    return send_file(
        final_pdf,
        as_attachment=True,
        download_name=f'{title}_bingo_card.pdf'
    )

@app.route('/api/artists')
def artists():
    return jsonify(get_top_artists())

@app.route('/api/top-tags')
def top_tags():
    return jsonify(get_top_tags())

@app.route('/api/tag-songs/<tag>')
def tag_songs(tag):
    return jsonify(get_tag_tracks(tag))

@app.route('/api/artists/<artist>')
def artist_tracks(artist):
    return jsonify(get_top_tracks(artist))

@app.route('/api/search')
def artist_search():
    artist = request.args.get('artist')
    return jsonify(get_top_tracks(artist))

@app.route('/api/recent_artists')
def artistslist():
    spotify = get_spotify()
    if spotify is None:
        return jsonify({'authenticated': False}), 401
    return jsonify({
        'authenticated': True,
        'artists':get_user_recent_artists(spotify)})

@app.route('/api/create_playlist', methods=['POST'])
def create_playlist():
    song_list = request.get_json()
    playlist = create_spotify_playlist(song_list)
    return jsonify({
        'success': True,
        'name': playlist['name'],
        "url": playlist["external_urls"]["spotify"]
    })

@app.route("/spotify/login")
def spotify_login():
    auth_url = oauth.get_authorize_url()
    session['spotify_auth_state'] = oauth.state
    
    response = redirect(auth_url)
    response.headers["Cache-Control"] = "no-store"
    
    return response

@app.route('/callback')
def spotify_callback():
    code = request.args.get('code')
    if not code:
        return "Authorization Failed", 400
    token_info = oauth.get_access_token(code)
    
    session['token_info'] = token_info
    return redirect('/')

if __name__ == '__main__':
    app.run(host="0.0.0.0")