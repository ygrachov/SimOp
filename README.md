### <li> Backend: Django 4.1.4, Python 3.9
### <li> Database: SQLLite
### <li> Frontend: HTML-5, Bootstrap-4, JavaScript

### GENERAL
This application is built on top of the SimPy library and simulates outbound operations during a call center 
shift.</p> The model takes input from a web form, records it in a database, and passes it to the init of the class 
CallCenter. The methods in this class are responsible for performing the simulation. Detailed documentation of the 
specific classes and functions can be found in the docstrings.<p> Once the simulation is completed, the user is redirected
to a results page where they can view their input and a link to download a CSV-formatted log file.</p> After downloading the
log file, the user's input and simulation results are automatically deleted from the database.


### manage.py:
The manage.py file is a command-line utility that allows you to interact with this application, primarily during the development process

### models.py:
models.py defines two models</p>
<li>a Django model called CreateInput. The model includes several fields that represent various aspects of a call center simulation and are expected to be input by the user
<li>class GlobalResults is a Django model that represents the results of a call center simulation. The class has several fields that store different aspects of the simulation results

### views.py:
<li>The InputForm is a ModelForm used to create a form for the CreateInput model. 
<li>The index function returns a context dictionary and renders the 'simulator/index.html' template which is the main page
<li>The CallCenter class represents a call center and is used to simulate a call center environment. It has several attributes and methods for managing the call center and its operations. 
<li>The IncomingCall class represents an instance of a call used in the simulation. 
<li>The launch function starts the simulation. 
<li>The Results class renders the output page when the simulation is completed. 
<li>The export_csv function exports the data from the GlobalResults model as a CSV file and returns it as an HTTP response

### urls.py:
The app_name variable is set to 'simulator' which is used to uniquely identify the URLs in this file among others in the project</p>

The urlpatterns list contains a series of path objects, each of which maps a URL to a view function. The URLs and the corresponding views are:</p>

<li>'' (the root URL of the project) is mapped to the index view. The name of this URL is 'main'.
<li>'form/' is mapped to the GetVars view, which is a class-based view. The name of this URL is 'form'.
<li>'launch' is mapped to the launch view. The name of this URL is 'launch'.
<li>'export/' is mapped to the display_results view. The name of this URL is 'export'.
<li>'download_csv' is mapped to the export_csv view. The name of this URL is 'csv'.</li></p>
When a user navigates to one of these URLs in their web browser, the corresponding view function will be executed, and the resulting HTML will be displayed in the browser.

### forms.py:
This file contains the InputForm class, which is a Django ModelForm that is used to handle user input for the CreateInput model.</p>
This class is a ModelForm that is generated from the CreateInput model.</p>
The fields attribute is set to 'all', which means that all fields in the CreateInput model will be included in the form. 

### templates: 
This folder contains the HTML templates that define the structure and layout of the pages that are displayed to the user. 

### static:
The static directory contains a collection of images used in the layout of pages.

### templatetags:
This directory contains a custom method which allows for the rendering of nicely formatted content from the database.

