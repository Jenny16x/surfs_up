from flask import Flask
#This __name__ variable denotes the name of the current function. 
# #You can use the __name__ variable to determine if your code is being run from the command line 
# #or if it has been imported into another piece of code. Variables with underscores before and after them 
# #are called magic methods in Python.
app = Flask(__name__)
#we need to define the starting point, also known as the root. To do this, we'll use the function @app.route('/')
#Notice the forward slash inside of the app.route? This denotes that we want to put our data at the root of our routes. 
# #The forward slash is commonly known as the highest level of hierarchy in any computer system.
## @app.route('/')

#create a function called hello_world()

@app.route('/')
def hello_world():
    return 'Hello world'


#Environment variables are essentially dynamic variables in your computer. 
# #They are used to modify the way a certain aspect of the computer operates. 
# #For our FLASK_APP environment variable, we want to modify the path that will run our app.py file 
# #so that we can run our file.

