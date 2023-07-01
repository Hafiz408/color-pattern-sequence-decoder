import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import pickle

df = pd.read_csv('/content/colors.csv').drop(columns=['Unnamed: 0'])

# shuffle dataset
df = df.sample(frac=1).reset_index(drop=True)

# split train and test data
y = df['Label']
x = df.drop('Label',axis=1)

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.33,random_state=42)

# Create and fit the logistic regression model
logreg = LogisticRegression()
logreg.fit(x_train, y_train)

# Make predictions on the test set
y_pred = logreg.predict(x_test)

# Evaluate the model performance
print(classification_report(y_test, y_pred))

# Save the model as a pickle file
filename = 'logistic_regression_model.pkl'
pickle.dump(logreg, open(filename, 'wb'))

# Load the saved model
filename = 'logistic_regression_model.pkl'
loaded_model = pickle.load(open(filename, 'rb'))

# Use the loaded model for predictions
# Example:
new_data = [[100, 50, 75]]  # New RGB values for prediction
predicted_class = loaded_model.predict(new_data)
print(predicted_class[0])

