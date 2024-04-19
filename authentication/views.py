from django.shortcuts import render

def authentication(request):
  return render(request, 'authentication.html')

def register(request):
  return render(request, 'register.html')

def login(request):
  return render(request, 'login.html')