from django.http.response import HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

# Create your views here.
@permission_required('core')
def administracion(request):
    return render(request,'admin.html')

def pag_404(request):
    return render(request,"header.html")
    