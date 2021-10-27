import pickle
from flask import Flask, request, jsonify, render_template
from model_files.ml_model import predict_mpg


app = Flask('mpg_prediction')

@app.route('/predict', methods=['POST'])
def predict():
    vehicle = request.get_json()
    print(vehicle)
    with open('./model_files/model.bin', 'rb') as f_in:
        model = pickle.load(f_in)
        f_in.close()
    predictions = predict_mpg(vehicle, model)

    result = {
        'mpg_prediction': list(predictions)
    }
    return jsonify(result)

@app.route('/ping', methods=['GET'])
def ping():
    return "Pinging Model!!"

@app.route('/', methods=['GET', 'POST'])
def accueil():
    cylinder=0
    prediction=0
    if request.method == 'POST':
        cylinder = request.form['Cylinder']
    
        vehicle_config = {
        'Cylinders': [4, 6, 8],
        'Displacement': [155.0, 160.0, 165.5],
        'Horsepower': [93.0, 130.0, 98.0],
        'Weight': [2500.0, 3150.0, 2600.0],
        'Acceleration': [15.0, 14.0, 16.0],
        'Model Year': [81, 80, 78],
        'Origin': [3, 2, 1] 
        }

        with open('./model_files/model.bin', 'rb') as f_in:
            model = pickle.load(f_in)
            f_in.close()
    
        prediction = predict_mpg(vehicle_config, model)
        print ('Prediction',prediction)
        
    return render_template("index.html", cyl=cylinder, predict=prediction.tolist())
    #return render_template("index.html")



