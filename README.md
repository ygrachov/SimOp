views.py:
InputForm is a ModelForm that is used to create a form for the CreateInput model.
index is a view function that returns an empty context dictionary and renders the 'simulator/index.html' template.
GetVars is a view class that handles HTTP GET and POST requests for the form page. It uses the InputForm to render the form template, and saves the form data to the CreateInput model when a POST request is received.
CallCenter is a class that represents a call center and is used to simulate a call center environment. It has several attributes and methods for managing the call center and its operations.
export_csv is a view function that exports the data from the GlobalResults model as a CSV file and returns it as an HTTP response.
