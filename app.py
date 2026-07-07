from flask import Flask, render_template, request
from src.bingo import create_bingo_card
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    
    title=request.form['title']
    songs = request.form['songs']
    number_of_sheets = request.form['number_of_sheets']
    
    song_list = [song.strip() for song in songs.splitlines() if song.strip()]
    
    print('songs received:', len(song_list))
    
    card = create_bingo_card(song_list)
    
    print(card)
    
    return 'Processed!'

if __name__ == '__main__':
    app.run(debug=True)