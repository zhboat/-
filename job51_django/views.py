from django.shortcuts import render


def hello(request):
    return render(request, 'index.html')
def login(request):
    return render(request, 'login.html')