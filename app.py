from flask import Flask, render_template, request
from src.bingo import create_bingo_card
from pathlib import Path
from src.excel import create_excel_card

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
    
    for i in range(number_of_sheets):
        card = create_bingo_card(song_list)
        
        output = temp_folder / f'{title}_{i+1}.xlsx'
        
        create_excel_card(card, title, template, output)
    
    return 'Processed!'

if __name__ == '__main__':
    app.run(debug=True)