import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#This __name__ variable denotes the name of the current function. 
# #You can use the __name__ variable to determine if your code is being run from the command line 
# #or if it has been imported into another piece of code. Variables with underscores before and after them 
# #are called magic methods in Python.
app = Flask(__name__)
#we need to define the starting point, also known as the root. To do this, we'll use the function @app.route('/')
#Notice the forward slash inside of the app.route? This denotes that we twant to put our data at the root of our routes. 
# #The forward slash is commonly known as the highest level of hierarchy in any computer system.
## @app.route('/')

#create a function called hello_world()

#@app.route('/')
#def hello_world():
#   return 'Hello world'


#Environment variables are essentially dynamic variables in your computer. 
# #They are used to modify the way a certain aspect of the computer operates. 
# #For our FLASK_APP environment variable, we want to modify the path that will run our app.py file 
# #so that we can run our file.

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
# reflect the database
Base.prepare(engine, reflect=True)
#With the database reflected, we can save our references to each table.
Measurement = Base.classes.measurement
Station = Base.classes.station
# create a session link from Python to our database with the following code
session = Session(engine)
#set up flask application name app
app = Flask(__name__)
#define the welcome route using the code below
@app.route("/")
#create a function welcome() with a return statement. Add this line to your code
#Next, add the precipitation, stations, tobs, and temp routes that we'll need for this module into our 
# #return statement. We'll use f-strings to display them for our investors:
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')
#To create the route, add the following code. Make sure that it's aligned all the way to the left.
@app.route("/api/v1.0/precipitation")
#Next, we will create the precipitation() function.
def precipitation():
    #calculates the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #a query to get the date and precipitation for the previous year.
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
      #We'll use jsonify() to format our results into a JSON structured file.
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
#a query that will allow us to get all of the stations in our database
def stations():
    #get all of the stations in our database
    results = session.query(Station.station).all()
    #We want to start by unraveling our results into a one-dimensional array. To do this, we want to use 
    #thefunction np.ravel(), with results as our parameter.
    #Next, we will convert our unraveled results into a list. To convert the results to a list, we will 
    # need to use the list function, which is list(), and then convert that array into a list. 
    # Then we'll jsonify the list and return it as JSON
    stations = list(np.ravel(results))
    return jsonify(stations=stations)
    
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
        #as before, unravel the results into a one-dimensional array and convert that array into a list. 
        # Then jsonify the list and return our results,
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
    
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
#We need to add parameters to our stats()function: a start parameter and an end parameter. F
# or now, set them both to None.
def stats(start=None, end=None):
     #With the function declared, we can now create a query to select the minimum, average, 
     # and maximum temperatures from our SQLite database. We'll start by just creating a list called sel, 
     # with the following code:
     sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
     #Since we need to determine the starting and ending date, add an if-not statement to our code. 
     # This will help us accomplish a few things. We'll need to query our database using the list that we 
     # just made. Then, we'll unravel the results into a one-dimensional array and convert them to a list. 
     # Finally, we will jsonify our results and return them.
     #In the following code, take note of the asterisk in the query next to the sel list. 
     # Here the asterisk is used to indicate there will be multiple results for our query: 
     # minimum, average, and maximum temperatures.
     if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
        #Now we need to calculate the temperature minimum, average, and maximum with the start and end dates. 
        # #We'll use the sel list, which is simply the data points we need to collect. 
        # #Let's create our next query, which will get our statistics data   
     results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
     temps = list(np.ravel(results))
     return jsonify(temps)
#After running this code, you'll be able to copy and paste the web address provided by Flask into a web browser. 
# Open /api/v1.0/temp/start/end route and check to make sure you get the correct result, which is:
#[null,null,null]
#This code tells us that we have not specified a start and end date for our range. Fix this by entering any 
# date in the dataset as a start and end date. The code will output the minimum, maximum, and average 
# temperatures. For example, let's say we want to find the minimum, maximum, and average temperatures for
#  June 2017. You would add the following path to the address in your web browser: /api/v1.0/temp/2017-06-01/2017-06-30


