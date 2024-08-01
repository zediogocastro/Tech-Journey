import pickle
import yaml


from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

model_file = 'models/model_C=1.0.bin'
schema_file = 'schema.yaml'

with open(schema_file, 'r') as f:
    SCHEMA = yaml.safe_load(f)['fields']

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

app = Flask('churn')
CORS(app)

# Function to convert string type to actual type
def str_to_type(type_str):
    if type_str == "int":
        return int
    elif type_str == "float":
        return float
    elif type_str == "str":
        return str
    else:
        raise ValueError(f"Unknown type: {type_str}")


# Validate and map input data
def validate_and_map_input(data):
    validated_data = {}
    for field, props in SCHEMA.items():
        value = data.get(field, props['default'])
        try:
            # Convert the value to the required type
            validated_data[field] = str_to_type(props['type'])(value)
            print(f"Field: {field} converted into {str_to_type(props['type'])}")
        except ValueError:
            validated_data[field] = props['default']  # Use default value if conversion fails
    return validated_data


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        customer = request.get_json()
        customer = validate_and_map_input(customer)

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