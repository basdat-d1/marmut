from django.shortcuts import render

def authentication(request):
  return render(request, 'authentication.html')

def register(request):
  return render(request, 'register.html')

def register_pengguna(request):
  return render(request, 'registration_form/register_pengguna.html')

def register_label(request):
  return render(request, 'registration_form/register_label.html')

def login(request):
  return render(request, 'login.html')