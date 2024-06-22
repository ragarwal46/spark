from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
def pounds_to_kg(pounds):
    return float(pounds) / 2.205

def inches_to_meters(feet, inches):
    total_inches = float(feet) * 12 + float(inches)
    return total_inches / 39.37

def convert(data):
    gender = {'Male': 1, 'Female': 0}
    yes_no = {'Yes': 1, 'No': 0}
    frequency = {'Frequently': 1, 'Sometimes': 2, 'Never': 3}
    transport = {'Automobile': 0, 'Bike': 1, 'Motorbike': 2,'Public Transport': 3, 'Walking': 4}
    new_data = [int(data[1]), inches_to_meters(data[2], data[3]), pounds_to_kg(data[4])]

    for item in data[5:9]:
        new_data.append(float(item))
    
    new_data.append(gender[data[0]])

    for item in data[9:13]:
        new_data.append(yes_no[item])

    new_data.append(frequency[data[13]])
    new_data.append(frequency[data[14]])
    new_data.append(transport[data[15]])

    return new_data

def interpret(number):
    levels = {0: 'are underweight', 1: 'are normal Weight', 2: 'have type 1 obesity', 3: 'have type 2 obesity', 
              4: 'have type 3 obesity', 5:'are little overweight', 6:'are over weight'}
    return levels[number]

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = convert(list(request.form.to_dict().values()))
        result = interpret(model.predict(np.array(data).reshape(1,-1))[0])
        return redirect(url_for('results', res = result))
    return render_template('index.html')

@app.route('/results', methods = ['POST', 'GET'])
def results():
    return render_template('results.html', res = request.args.get('res'))

if __name__ == '__main__':
    app.run(debug=True)