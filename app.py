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
    levels = {0: 'are underweight', 1: 'are normal weight', 2: 'have type 1 obesity', 3: 'have type 2 obesity', 
              4: 'have type 3 obesity', 5:'are a little overweight', 6:'are overweight'}
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
    tips = {'are underweight': 'Being underweight can lead to various health issues, such as a weakened immune system, osteoporosis, and fertility problems. To manage this, consider increasing your calorie intake with nutrient-rich foods, incorporating more protein and healthy fats into your diet, and engaging in strength training exercises to build muscle mass. It is also essential to consult a healthcare provider to check for any underlying health conditions.',
            'are normal weight': 'Being of normal weight means your body weight is within the healthy range for your height. This balance between caloric intake and expenditure supports your overall well-being. To maintain this, keep a balanced diet with a variety of nutrients, stay active with regular exercise, and monitor your weight and health markers periodically. Additionally, managing stress and getting adequate sleep are crucial for maintaining your health.',
            'have type 1 obesity': 'To manage this, adopt a healthy eating plan with reduced caloric intake, increase your physical activity to at least 150 minutes of moderate exercise per week, and seek support from a healthcare provider for personalized advice. Joining a weight management program can also provide additional support.',
            'have type 2 obesity': 'Managing this condition involves following a structured weight loss program with dietary changes and exercise, considering behavioral therapy to support lifestyle changes, and consulting with a healthcare provider about possible medications or surgery. Regularly monitoring your health and following medical advice is crucial.',
            'have type 3 obesity': 'To address this, engage in a comprehensive weight loss plan under medical supervision, explore all treatment options including bariatric surgery if recommended, and adopt healthy eating habits along with consistent physical activity. Close cooperation with healthcare providers is essential to manage and reduce health risks effectively.',
            'are a little overweight': 'While this may not pose significant risks yet, it is important to manage it to avoid future health issues. Make minor adjustments to your diet by reducing sugary and high-fat foods, increase your daily physical activity like walking or light exercise, and monitor your weight regularly to ensure it stays within a healthy range. Staying hydrated and getting enough sleep also supports weight management.',
            'are overweight': 'To address this, implement a balanced diet with controlled portion sizes, engage in regular physical activity aiming for at least 150 minutes of exercise per week, set realistic weight loss goals, and track your progress. Seeking advice from a healthcare provider can offer personalized guidance to help you manage your weight effectively.'}
    results = request.args.get('res')
    return render_template('results.html', res = results, details = tips[results])

if __name__ == '__main__':
    app.run(debug=True)