from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from .models import *

def user_is_admin(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_superuser and (not hasattr(request.user, 'customerregistration')):
            return redirect('/admin/')
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_technician(function):
    def wrap(request, *args, **kwargs):
        if request.user.customerregistration.role == 'technician':
            return function(request, *args, **kwargs)
        else:
            return redirect('dashboard')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def user_is_customer(function):
    def wrap(request, *args, **kwargs):
        if request.user.customerregistration.role == 'customer':
            return function(request, *args, **kwargs)
        else:
            return redirect('dashboard')
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap