from django.shortcuts import render
from django.contrib import messages



# Create your views here.


def index(request):
    print(f'{messages}')
    return render(request, 'home/index.html')
