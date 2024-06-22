from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    protein = request.form['protein']
    fat = request.form['fat']
    carbs = request.form['carbs']
    return f"Received macros - Protein: {protein}g, Fat: {fat}g, Carbohydrates: {carbs}g"

if __name__ == '__main__':
    app.run(debug=True)
	