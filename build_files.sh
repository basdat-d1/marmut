#!/bin/bash
# Build script for Vercel deployment

echo "🔧 Running Django tests..."
python test_vercel.py

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!" 