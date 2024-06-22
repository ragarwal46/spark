import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import pickle
# Creating dataframe from csv file
df = pd.read_csv('data.csv')

# Converting categorical data into numberic data
unencoded = ['Gender', 'family_history', 'FAVC', 'SMOKE', 'SCC', 'CAEC', 'CALC', 'MTRANS', 'LEVEL']
for label in unencoded:
    conv = LabelEncoder()
    encoded = conv.fit_transform(df[label])
    df.drop(label , axis = 1, inplace = True)
    df[label] = encoded

attributes = df.drop('LEVEL', axis = 1)
weight_level = df['LEVEL']

# Testing accuracy of model
a_train, a_test, w_train, w_test = model_selection.train_test_split(attributes, weight_level, test_size = 0.2)

decision_tree = tree.DecisionTreeClassifier()
decision_tree.fit(a_train, w_train)

print(decision_tree.score(a_test, w_test))
# Fitting model with all data
decision_tree.fit(attributes, weight_level)
print(decision_tree.predict(np.array([21.0, 1.8, 100, 3.0, 2.0, 0.0, 1.0, 1, 0, 0, 2, 0, 0, 3, 3]).reshape(1,-1)))

pickle.dump(decision_tree, open('model.pkl', 'wb'))