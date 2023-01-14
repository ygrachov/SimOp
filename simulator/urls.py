from django.urls import path
from .views import *

app_name = 'simulator'
urlpatterns = [
    path('', index, name='main'),
    path('form/', GetVars.as_view(), name='form'),
    path('launch', launch, name='launch'),
    path('export/', display_results, name='export'),
    path('download_csv', export_csv, name='csv')
]
