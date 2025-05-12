from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .models import UserRole

# Decorator to check if user is an HR manager
def hr_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role == UserRole.HR_MANAGER or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        except:
            return HttpResponseForbidden("You don't have permission to access this page.")
    
    return wrapper

# Decorator to check if user is a restaurant manager
def restaurant_manager_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role == UserRole.RESTAURANT_MANAGER or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        except:
            return HttpResponseForbidden("You don't have permission to access this page.")
    
    return wrapper

# Decorator to check if user is an admin
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role == UserRole.ADMIN or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        except:
            return HttpResponseForbidden("You don't have permission to access this page.")
    
    return wrapper

# Decorator to check if user is a candidate
def candidate_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            if request.user.profile.role == UserRole.CANDIDATE or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("You don't have permission to access this page.")
        except:
            return HttpResponseForbidden("You don't have permission to access this page.")
    
    return wrapper
