#import  libraries
from unicodedata import name
from flask import Flask, redirect , render_template, request, url_for , redirect , escape
import pickle
import numpy as np
import pandas as pd 
import datetime

# Making function for check and modal
def multiFunction():
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
        pulse_pressure=Systolic-Diastolic

        # preprocessing for data


        # convert Birthdate to days
        checkdate = datetime.datetime.strptime( bdate, "%Y-%m-%d")
        bdate = (datetime.datetime.now()-checkdate).days
        print(bdate)
        
        # Random variables

        # gender
        if(gender == "Male"):
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

        # prediction_input=[20411.0, 1.0, 168.0, 86.0, 120.0, 80.0, 40.0, 1.0, 1.0, 0.0, 0.0, 1.0]
        prediction_input=[bdate,gender,height,weight ,Systolic,Diastolic,pulse_pressure,Cholesterol,Glucose,Smoking,Alcoholintake,Physicalactivity]
        # prediction= model.predict([[bdate,height,weight,gender ,Systolic,Diastolic,Cholesterol,Glucose,Smoking,Alcoholintake,Physicalactivity]])
        prediction= model.predict(np.array(prediction_input).reshape(1,-1))
        prediction_probability =model.predict_proba(np.array(prediction_input).reshape(1,-1))
        print(prediction)

        # Assig. data for user
        if (prediction== 0):
            my_prediction = "Healthy"
            my_probability = "{:.2f}".format(prediction_probability[0,0]*100)

        else:
            my_prediction= "UN Healthy with CardioVascular Disease"
            my_probability = "{:.2f}".format(prediction_probability[0,1]*100)

        return render_template("modal.html",  patientName= name , patientSname=sname ,prediction_text= my_prediction, prediction_text_probability=my_probability)
        # return render_template("modal.html",  patientName= name , patientSname=sname ,prediction_text= my_prediction,prediction_input=prediction_input, prediction_text_probability=my_probability)

    else:
        return render_template("check.html")   

# End of function

# import model
flasklink = Flask(__name__)
model = pickle.load(open('Machine_Learning/RandomModelClassifier.pkl','rb'))

# Home page
@flasklink.route("/") 
def Home():

    return render_template("Home.html", pagetitle = "home", custom_css = "home")  


@flasklink.route("/check") 
def check():
    return multiFunction()

# prediction page
@flasklink.route("/modal" , methods =['POST','GET']) #domain 
def modal():
    return multiFunction()

# About page
@flasklink.route("/about") 
def about():
    return render_template("about.html") 

# clean file 
@flasklink.route("/clean") 
def clean():
    return render_template("AnalysisClean.html") 

# not clean file
@flasklink.route("/not_clean") 
def notclean():
    return render_template("AnalysisNotClean.html") 


# run our programe
if __name__== "__main__":  #for make this content appear when file open directly not importent from another file
    flasklink.run(debug=True, port=9000)


