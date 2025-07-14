#!/bin/bash
# Build script for Vercel deployment

echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!" 