from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def customer_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'customer':
            return redirect('auth_page')
        return view_func(request, *args, **kwargs)
    return wrapper


def farmer_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'farmer':
            return redirect('auth_page')
        return view_func(request, *args, **kwargs)
    return wrapper
