from flask import Flask, render_template, request, send_file, jsonify
from src.bingo import create_bingo_card
from pathlib import Path
from src.excel import create_excel_card
from src.pdf import convert_excel_to_pdf, merge_pdfs
from src.cleanup import clear_folder
from src.lastfm import get_top_artists, get_top_tracks


app = Flask(__name__)

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

@app.route('/api/artists/<artist>')
def artist_tracks(artist):
    return jsonify(get_top_tracks(artist))

@app.route('/api/search')
def artist_search():
    artist = request.args.get('artist')
    return jsonify(get_top_tracks(artist))

if __name__ == '__main__':
    app.run(host="0.0.0.0")