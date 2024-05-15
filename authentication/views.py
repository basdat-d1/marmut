import uuid
import random
import datetime
from utils.query import connectdb
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db import connection
from django.db.backends.utils import CursorWrapper
from django.http import HttpResponseRedirect

def authentication(request):
  return render(request, 'authentication.html')

def register(request):
  return render(request, 'register.html')

@connectdb
def is_premium(cursor: CursorWrapper, email):
    cursor.execute("SELECT * FROM PREMIUM WHERE email = %s", [email])
    user = cursor.fetchone()

    return True if user else False
      
@connectdb
def register_pengguna(cursor: CursorWrapper, request):
  context = {
    'is_podcaster': False,
    'is_artist': False,
    'is_songwriter': False
  }

  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    nama = request.POST.get('nama')
    gender = request.POST.get('gender')
    tempat_lahir = request.POST.get('tempat_lahir')
    tanggal_lahir = request.POST.get('tanggal_lahir')
    kota_asal = request.POST.get('kota_asal')
    roles = request.POST.getlist('role')

    gender_info = 0 if gender == 'Perempuan' else 1
    is_verified = bool(roles)
    

    with connection.cursor() as cursor:
      # Cek apakah email sudah ada di tabel AKUN atau LABEL
      cursor.execute("SELECT * FROM AKUN WHERE email = %s", [email])
      user = cursor.fetchone()
      cursor.execute("SELECT * FROM LABEL WHERE email = %s", [email])
      label = cursor.fetchone()

      # Jika email sudah ada
      if user or label:
          messages.error(request, "Email sudah pernah didaftarkan.")
          return render(request, 'registration_form/register_pengguna.html', {'form': request.POST})

      # Cek panjang password minimal 8 karakter
      if len(password) < 8:
          messages.error(request, "Password minimal harus 8 karakter.")
          return render(request, 'registration_form/register_pengguna.html', {'form': request.POST})
      
      cursor.execute(
        """INSERT INTO AKUN(email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s)""", 
            (email, password, nama, gender_info, tempat_lahir, tanggal_lahir, is_verified, kota_asal)
      )
    
      for role in roles:
        if role == "Podcaster":
          cursor.execute("INSERT INTO PODCASTER(email) VALUES (%s)", [email])
          context['is_podcaster'] = True

        elif role == "Artist":
          id_artist = str(uuid.uuid4())
          cursor.execute('SELECT id FROM PEMILIK_HAK_CIPTA')
          ids = cursor.fetchall()
          id_pemilik_hak_cipta = str(random.choice(ids)[0])
          cursor.execute("INSERT INTO ARTIST(id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)",
                          (id_artist, email, id_pemilik_hak_cipta))
          context['is_artist'] = True

        elif role == "Songwriter":
          id_songwriter = str(uuid.uuid4())
          cursor.execute('SELECT id FROM PEMILIK_HAK_CIPTA')
          ids = cursor.fetchall()
          id_pemilik_hak_cipta = str(random.choice(ids)[0])
          cursor.execute("INSERT INTO SONGWRITER(id, email_akun, id_pemilik_hak_cipta) VALUES (%s, %s, %s)",
                          (id_songwriter, email, id_pemilik_hak_cipta))
          context['is_songwriter'] = True
      
      messages.success(request, 'Your account has been successfully created!')
      return redirect('authentication:login')

  return render(request, 'registration_form/register_pengguna.html')

@connectdb
def register_label(cursor: CursorWrapper, request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    nama = request.POST.get('nama')
    kontak = request.POST.get('kontak')
    id_label = str(uuid.uuid4())

    with connection.cursor() as cursor:
      # Cek apakah email sudah ada di tabel AKUN atau LABEL
      cursor.execute("SELECT * FROM AKUN WHERE email = %s", [email])
      user = cursor.fetchone()
      cursor.execute("SELECT * FROM LABEL WHERE email = %s", [email])
      label = cursor.fetchone()

      # Jika email sudah ada
      if user or label:
          messages.error(request, "Email sudah pernah didaftarkan.")
          return render(request, 'registration_form/register_label.html', {'form': request.POST})
      
      # Cek panjang password minimal 8 karakter
      if len(password) < 8:
          messages.error(request, "Password minimal harus 8 karakter.")
          return render(request, 'registration_form/register_label.html', {'form': request.POST})
            
      cursor.execute('SELECT id FROM PEMILIK_HAK_CIPTA')
      ids = cursor.fetchall()
      id_pemilik_hak_cipta = str(random.choice(ids)[0])

      cursor.execute(
        """INSERT INTO LABEL(id, nama, email, password, kontak, id_pemilik_hak_cipta) VALUES 
            (%s, %s, %s, %s, %s, %s)""", 
            (id_label, nama, email, password, kontak, id_pemilik_hak_cipta)
      )
      
    messages.success(request, 'Your account has been successfully created!')
    return redirect('authentication:login')
  
  return render(request, 'registration_form/register_label.html')

@connectdb
def login(cursor: CursorWrapper, request):
  context = {
    'is_premium': False,
    'is_logged_in': False 
  }

  if "email" in request.session:
    return redirect('dashboard:dashboard_podcaster')

  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')

    with connection.cursor() as cursor:
      cursor.execute(f"SELECT * FROM AKUN WHERE email = '{email}' AND password = '{password}'")
      user_pengguna = cursor.fetchone()

      cursor.execute(f"SELECT * FROM LABEL WHERE email = '{email}' AND password = '{password}'")
      user_label = cursor.fetchone()

      # Kalo email atau password salah
      if not user_pengguna or not user_label:
        context["message"] = "Email atau password salah"
        return render(request, "login.html", context)

      if user_pengguna:
        request.session["registered_as"] = "pengguna"

        if is_premium(cursor, email):
          context['is_premium'] = True
      elif user_label:
        request.session["registered_as"] = "label"

      request.session["email"] = email
      request.session['is_logged_in'] = True
      response = HttpResponseRedirect(reverse('dashboard:dashboard_podcaster'))
      response.set_cookie('last_login', str(datetime.datetime.now()))
      return response
      
  return render(request, 'login.html', context)

def logout(request):
    request.session.flush()
    response = HttpResponseRedirect(reverse('authentication:authentication'))
    response.delete_cookie('last_login')

    return response