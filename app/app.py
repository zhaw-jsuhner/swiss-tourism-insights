from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', image='static/price_vs_rating.png')

if __name__ == '__main__':
    app.run(debug=True)