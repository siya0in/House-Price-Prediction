import numpy as np  # Import numpy for handling missing values

@app.route('/predict', methods=['POST'])
def predict():
    bedrooms = request.form.get('numberOfRooms')
    bathrooms = request.form.get('bathroom')
    size = request.form.get('squareMeters')
    zipcode = request.form.get('cityCode')

    # Replace empty strings with None
    bedrooms = None if bedrooms == '' else bedrooms
    bathrooms = None if bathrooms == '' else bathrooms
    size = None if size == '' else size
    zipcode = None if zipcode == '' else zipcode

    # Create a DataFrame with the input data
    input_data = pd.DataFrame([[bedrooms, bathrooms, size, zipcode]],
                               columns=['numberOfRooms', 'bathroom', 'squareMeters', 'cityCode'])

    print("Input Data:")
    print(input_data)

    # Convert 'baths' column to numeric with errors='coerce'
    input_data['bathroom'] = pd.to_numeric(input_data['bathroom'], errors='coerce')

    # Convert input data to numeric types
    input_data = input_data.astype({'numberOfRooms': float, 'bathroom': float, 'squareMeters': float, 'cityCode': float})

    # Handle missing values
    input_data.fillna(0, inplace=True)  # Replace missing values with 0, you can choose a different strategy

    print("Processed Input Data:")
    print(input_data)

    # Predict the price
    prediction = pipe.predict(input_data)[0]

    return str(prediction)





from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)
data = pd.read_csv('final_dataset.csv')
pipe = pickle.load(open("RidgeModel.pkl", 'rb'))

@app.route('/')
def index():
    bedrooms = sorted(data['numberOfRooms'].unique())
    bathrooms = sorted(data['bathroom'].unique())
    sizes = sorted(data['squareMeters'].unique())
    zip_codes = sorted(data['cityCode'].unique())

    return render_template('index.html', bedrooms=bedrooms, bathrooms=bathrooms, sizes=sizes, zip_codes=zip_codes)

@app.route('/predict', methods=['POST'])
def predict():
    bedrooms = request.form.get('numberOfRooms')
    bathrooms = request.form.get('bathroom')
    size = request.form.get('squareMeters')
    zipcode = request.form.get('cityCode')

    # Create a DataFrame with the input data
    input_data = pd.DataFrame([[bedrooms, bathrooms, size, zipcode]],
                               columns=['numberOfRooms', 'bathroom', 'squareMeters', 'cityCode'])

    print("Input Data:")
    print(input_data)

    # Convert 'baths' column to numeric with errors='coerce'
    input_data['bathroom'] = pd.to_numeric(input_data['bathroom'], errors='coerce')

    # Convert input data to numeric types
    input_data = input_data.astype({'numberOfRooms': int, 'bathroom': float, 'squareMeters': float, 'cityCode': int})

    # Predict the price
    prediction = pipe.predict(input_data)[0]

    return str(prediction)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

