#!/usr/bin/env python
"""
Test script to verify Django app can start properly for Vercel deployment
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marmut_app.settings')

# Configure Django
django.setup()

# Test basic Django functionality
from django.core.wsgi import get_wsgi_application
from django.conf import settings

print("✅ Django settings loaded successfully")
print(f"✅ DEBUG mode: {settings.DEBUG}")
print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
print(f"✅ DATABASE: {settings.DATABASES['default']['ENGINE']}")

# Test WSGI application
application = get_wsgi_application()
print("✅ WSGI application created successfully")

# Test static files
if os.path.exists(settings.STATIC_ROOT):
    print(f"✅ Static files directory exists: {settings.STATIC_ROOT}")
else:
    print(f"⚠️  Static files directory does not exist: {settings.STATIC_ROOT}")

print("✅ All tests passed! Django app is ready for Vercel deployment.") 