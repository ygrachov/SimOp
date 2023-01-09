### views.py:
<li>The InputForm is a ModelForm used to create a form for the CreateInput model. 
<li>The index function returns an empty context dictionary and renders the 'simulator/index.html' template. 
<li>The GetVars view class handles HTTP GET and POST requests for the form page. It uses the InputForm to render the form template and saves the form data to the CreateInput model when a POST request is received. 
<li>The EditVars and ConfirmVars views are used to edit user inputs. 
<li>The CallCenter class represents a call center and is used to simulate a call center environment. It has several attributes and methods for managing the call center and its operations. 
<li>The IncomingCall class represents an instance of a call used in the simulation. 
<li>The launch function starts the simulation. 
<li>The Results class renders the output page when the simulation is completed. 
<li>The export_csv function exports the data from the GlobalResults model as a CSV file and returns it as an HTTP response
