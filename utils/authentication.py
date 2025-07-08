from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def require_authentication(view_func):
    """
    Custom authentication decorator that checks session without using Django ORM
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated via session
        user_email = request.session.get('user_email')
        
        if not user_email:
            return Response({
                'detail': 'Authentication credentials were not provided.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Add user info to request for easy access
        request.user_email = user_email
        request.user_type = request.session.get('user_type', 'user')
        request.user_roles = request.session.get('user_roles', ['user'])
        request.is_premium = request.session.get('is_premium', False)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper

def allow_any(view_func):
    """
    Decorator for views that don't require authentication
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    
    return wrapper 