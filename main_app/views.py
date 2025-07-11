from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')