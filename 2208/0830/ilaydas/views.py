from django.shortcuts import render

# Create your views here.

def ff(request):
    return render(request, 'ff.html')
