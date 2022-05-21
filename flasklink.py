#import  libraries
from unicodedata import name
from flask import Flask, redirect , render_template, request, url_for , redirect , escape
import pickle
import numpy as np
import pandas as pd 
import datetime

# import model
flasklink = Flask(__name__)
model = pickle.load(open('RandomModelClassifier.pkl','rb'))

# Home page
@flasklink.route("/") 
def Home():

    return render_template("Home.html", pagetitle = "home", custom_css = "home")  


# prediction page
@flasklink.route("/check" , methods =['POST','GET']) #domain 
def check():

    # getting data from user
     if request.method == 'POST':
        name = request.form['name']
        sname = request.form['sname']
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        bdate = request.form['bdate']
        gender = request.form['gender']
        Cholesterol = request.form['Cholesterol']
        Glucose =request.form['Glucose']
        Smoking = request.form['Smoking']
        Alcoholintake = request.form['Alcoholintake']
        Physicalactivity =request.form['Physicalactivity']
        Systolic = float(request.form['Systolic'])
        Diastolic = float(request.form['Diastolic'])

        # preprocessing for data


        # convert Birthdate to days
        checkdate = datetime.datetime.strptime("0001-01-01", "%Y-%m-%d")
        bdate = (datetime.datetime.now()-checkdate).days
        print(bdate)
        
        # Random variables

        # gender
        if(gender == "male"):
            gender = 1.0
        else:
            gender= 2.0  

        # cholesterol
        if(Cholesterol == "Normal"):
            Cholesterol = 1.0
        elif(Cholesterol == "Above normal"):
            Cholesterol= Cholesterol.replace("Above normal","2.0") 
        else:
           Cholesterol= Cholesterol.replace("Well above normal","3.0")    

        # glucose
        if(Glucose == "Normal"):
            Glucose= 1.0
        elif(Glucose == "Above normal"):
            Glucose= Glucose.replace("Above normal","2.0")  
        else:
           Glucose= Glucose.replace("Well above normal","3.0") 
        
        # smoking
        if(Smoking == "Yes"):
            Smoking = 1.0
        else:
            Smoking= 0.0 

        # alcoholintake
        if(Alcoholintake == "Yes"):
            Alcoholintake = 1.0
        else:
            Alcoholintake= 0.0 

        # phisical activity
        if(Physicalactivity == "Yes"):
            Physicalactivity = 1.0
        else:
            Physicalactivity= 0.0                   

        # get prediction from ML model
        prediction= model.predict([[bdate,height,weight,gender ,Systolic,Diastolic,Cholesterol,Glucose,Smoking,Alcoholintake,Physicalactivity]])
        
        print(prediction)

        # Assig. data for user
        if (prediction== 0):
            my_prediction = "Healthy"
        else:
            my_prediction= "unHealthy"

        render_template("check.html",  patientName= name , patientSname=sname ,prediction_text= my_prediction )

     else:
         return render_template("check.html")     

              

# run our programe
if __name__== "__main__":  #for make this content appear when file open directly not importent from another file
    flasklink.run(debug=True, port=9000)


