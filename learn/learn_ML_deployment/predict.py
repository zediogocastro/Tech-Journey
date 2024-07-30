import pickle

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

model_file = 'models/model_C=1.0.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = Flask('churn')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        customer = request.get_json()
        print("Received customer data:", customer)

        X = dv.transform([customer])
        print(f"Customer real X: {X}")
        y_pred = model.predict_proba(X)[0, 1]
        churn = y_pred >= 0.5

        result = {
            'churn_probability': float(y_pred),
            'churn': bool(churn)
        }
        print("Prediction result:", result)
        return jsonify(result)
    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)