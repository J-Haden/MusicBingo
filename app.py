from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    
    title=request.form['title']
    songs = request.form['songs']
    number_of_sheets = request.form['number_of_sheets']
    
    print('title:', title)
    print('Number of sheets:', number_of_sheets)
    print('Songs:')
    print(songs)
    
    return 'Data received!'

if __name__ == '__main__':
    app.run(debug=True)