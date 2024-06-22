from flask import Flask, render_template, request, redirect, url_for
import pickle
import numpy as np
from sklearn import tree

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
def pounds_to_kg(pounds):
    return float(pounds) / 2.205

def inches_to_meters(feet, inches):
    total_inches = float(feet) * 12 + float(inches)
    return total_inches / 39.37

def convert(data):
    print(data)
    gender = {'Male': 1, 'Female': 0}
    yes_no = {'Yes': 1, 'No': 0}
    frequency = {'Frequently': 1, 'Sometimes': 2, 'No': 3}
    transport = {'Automobile': 0, 'Bike': 1, 'Motorbike': 2,'Public Transport': 3, 'Walking': 4}
    new_data = [gender[data[0]], int(data[1]), inches_to_meters(data[2], data[3]), pounds_to_kg(data[4])]

    for item in data[5:9]:
        new_data.append(float(item))

    for item in data[9:13]:
        new_data.append(yes_no[item])

    new_data.append(frequency[data[13]])
    new_data.append(frequency[data[14]])
    new_data.append(transport[data[15]])
    
    return new_data

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        data = convert(list(request.form.to_dict().values()))
        print(model.predict(np.array(data).reshape(1,-1))[0])

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)