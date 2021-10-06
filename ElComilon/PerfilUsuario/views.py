from django.shortcuts import render
from Login.models import Cliente

# Create your views here.
def Usertemplate(request): 
    return render(request, 'User.html')