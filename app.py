from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


def pounds_to_kg(pounds):
    return pounds / 2.205

def inches_to_meters(feet, inches):
    total_inches = feet * 12 + inches
    return total_inches / 39.37
