from django.shortcuts import render

# Create your views here.
def menuProveedor(request,id):
    print(id)
    return render (request,'menuProveedor.html')