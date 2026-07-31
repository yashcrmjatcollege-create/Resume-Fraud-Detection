from sklearn.linear_model import LogisticRegression
import numpy as np

X = np.array([
    [1, 0.1],
    [3, 0.4],
    [5, 0.8],
    [0, 0.05],
    [6, 0.9]
])

y = [0, 0, 1, 0, 1]  # 0 = Genuine, 1 = Fraud

model = LogisticRegression()
model.fit(X, y)

def predict_fraud(buzzwords, similarity):
    prediction = model.predict([[buzzwords, similarity]])
    return "Fraudulent" if prediction[0] == 1 else "Genuine"