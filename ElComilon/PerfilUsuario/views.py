from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
def Usertemplate(request): 
    return render(request, 'User.html')