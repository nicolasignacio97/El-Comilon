from django.shortcuts import render

# Create your views here.
def administracion(request):
    return render(request,'admin.html')
    