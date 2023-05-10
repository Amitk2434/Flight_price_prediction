from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import xgboost
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("rf_bst_modl.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

##@app.route("/pre", methods = ["GET", "POST"])
##@cross_origin()
##def pre():
 ##   return render_template("pre.html")

@app.route("/proto", methods = ["GET", "POST"])
@cross_origin()
def proto():
    return render_template("proto.html")

@app.route("/pre", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == 'POST':

        #Date of Journey
        date_dep = request.form["Dep_Time"]
        journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)
        # Print ("Journey Date : ", Journey_day, Journey_month)

        #Departure
        Dep_Time_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_Time_minute = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

         # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_Time_hour = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_Time_minute = int(pd.to_datetime(date_arr, format ="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        # Duration
        Duration_hour = abs(Arrival_Time_hour - Dep_Time_hour)
        Duration_minutes = abs(Arrival_Time_minute - Dep_Time_minute)
        # print("Duration : ", dur_hour, dur_min)

        # Total Stops
        Total_Stops = int(request.form["stops"])
        # print(Total_stops)


        airline=request.form['airline']
        if(airline=='Jet Airways'):
            airline = 10

        elif (airline=='Indigo'):
            airline = 3

        elif (airline=='AirIndia'):
            airline = 7

        elif (airline=='SpiceJet'):
            airline = 1

        elif (airline=='Vistara'):
            airline = 5

        elif (airline=='GoAir'):
            airline = 5

        elif (airline=='Multiple Carriers'):
            airline = 8

        else:
            airline = 2

        Source = request.form["Source"]
        if(Source == 'Delhi'):
            Source_Delhi = 1
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0
            Source_Bangalore = 0

        elif (Source == 'Kolkata'):
            Source_Delhi = 0
            Source_Kolkata = 1
            Source_Mumbai = 0
            Source_Chennai = 0

        elif (Source == 'Mumbai'):
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 1
            Source_Chennai = 0
            Source_Bangalore = 0

        elif (Source == 'Chennai'):
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 1
            Source_Bangalore = 0

        elif(Source == 'Bangalore'):
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0
            Source_Bangalore = 1


        else:
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0
            Source_Bangalore = 0

        destination = request.form["Destination"]
        if (destination == 'Bangalore'):
            destination = 3

        elif (destination == 'Delhi'):
            destination = 2

        elif (destination == 'Cochin'):
            destination = 4

        elif (destination == 'Kolkata'):
            destination = 0

        elif (destination == 'Hyderabad'):
            destination = 1

        else:
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0
            Destination_Bangalore = 0


        prediction=model.predict([[
            Total_Stops,
            journey_day,
            journey_month,
            Dep_Time_hour,
            Dep_Time_minute,
            Arrival_Time_hour,
            Arrival_Time_minute,
            Duration_hour,
            Duration_minutes,
            airline,
            Source_Chennai,
            Source_Delhi,
            Source_Kolkata,
            Source_Mumbai,
            Source_Bangalore,
            destination

            #Destination_Cochin,
            #Destination_Delhi,
            #Destination_Kolkata,
            #Destination_Hyderabad,
        ]])


        output=round(prediction[0],2)

        return render_template('pre.html', prediction_text = "Your flight price for {} from {} to {} will be Rs: {}".format(request.form['airline'], Source, request.form["Destination"], output))

    return render_template("pre.html")


if __name__ == "__main__":
    app.run(debug=True)



