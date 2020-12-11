# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 16:30:21 2020

@author: DELL
"""
from flask import Flask, render_template, request, jsonify
import json
import pickle
import numpy as np

columns = None
model = None


app = Flask(__name__)
with open("columns.json", "r") as f:
    columns = json.load(f)["data_columns"]
clf = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/carname')
def carname():
    return jsonify(columns[11:-1])

@app.route('/fueltype')
def fueltype():
    return jsonify(columns[4:7])

@app.route('/sellertype')
def sellertype():
    return jsonify(columns[7:9])


@app.route('/transmission')
def transmission():
    return jsonify(columns[9:11])


@app.route("/predict", methods=['POST'])
def predict():
    Present_Price = float(request.form['Present_Price'])
    Kms_Driven = int(request.form['Kms_Driven'])
    year = int(request.form['year'])
    Car_Name = request.form['Car_Name']
    Fuel_Type 	 = request.form['Fuel_Type']
    Seller_Type = request.form['Seller_Type']
    Transmission = request.form['Transmission']
    
    
    Car_Name_ind = columns.index(Car_Name.lower())
    Fuel_Type_ind = columns.index(Fuel_Type.lower())
    Seller_Type_ind = columns.index(Seller_Type.lower())
    Transmission_ind = columns.index(Transmission.lower())
    
    data = np.zeros(len(columns))
    data[0] = Present_Price
    data[1] = Kms_Driven
    data[3] = year
    data[Car_Name_ind] = 1
    data[Fuel_Type_ind] = 1
    data[Seller_Type_ind] = 1
    data[Transmission_ind] = 1
    
    prediction = clf.predict([data])
    
    output = round(prediction[0], 2)
    
    return render_template('index.html', prediction='The selling price is {} Lakhs (INR)'.format(output))
    

    
if __name__=="__main__":
    app.run(debug=True)