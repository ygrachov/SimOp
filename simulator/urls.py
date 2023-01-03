from django.urls import path
from .views import *

app_name = 'simulator'
urlpatterns = [
    path('', index, name='main'),
    path('form/', GetVars.as_view(), name='form'),
    path('sucsess/', ConfirmVars.as_view(), name='success'),
    path('<int:pk>/update', EditVars.as_view(), name='update'),
    path('/',launch, name='launch'),
    path('export/', export_csv, name='export')
]