from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from farmer.models import Product, FarmerProfile
from farmer.forms import SignupForm
from .models import CustomUser
from .decorators import customer_required, farmer_required


# ================= HOME =================
def index(request):
    return render(request, 'index.html')


# ================= AUTH PAGE (LOGIN + SIGNUP) =================
def auth_page(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        # ---------- SIGNUP ----------
        if form_type == 'signup':
            form = SignupForm(request.POST)

            if form.is_valid():
                data = form.cleaned_data

                # Create CustomUser with role
                user = CustomUser.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password'],
                    role=data['role']
                )

                # Create FarmerProfile if farmer
                if data['role'] == 'farmer':
                    FarmerProfile.objects.create(
                        user=user,
                        phone=data['phone'],
                        location=''
                    )

                login(request, user)
                return redirect('role_redirect')

            else:
                # Form invalid — pass form with errors back to template
                return render(request, 'signup.html', {
                    'form': form,
                    'active_tab': 'signup'
                })

        # ---------- LOGIN ----------
        if form_type == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('role_redirect')
            else:
                return render(request, 'signup.html', {
                    'form': SignupForm(),
                    'login_error': 'Invalid username or password',
                    'active_tab': 'login'
                })

    # GET request
    return render(request, 'signup.html', {
        'form': SignupForm(),
        'active_tab': 'signup'
    })


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect('auth_page')


# ================= ROLE BASED REDIRECT =================
@login_required
def role_redirect(request):
    if request.user.role == 'farmer':
        return redirect('farmer_dashboard')
    elif request.user.role == 'customer':
        return redirect('customer_dashboard')
    return redirect('auth_page')


# ================= FARMER DASHBOARD =================
@login_required
@farmer_required
def farmer_dashboard(request):
    return render(request, 'farmer/farmer_dashboard.html')


# ================= CUSTOMER DASHBOARD =================
@login_required
@customer_required
def customer_dashboard(request):
    return render(request, 'customer/customer_dashboard.html')


# ================= SHOP LIST =================
def shop(request):
    products = Product.objects.select_related('farmer').all()

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'shop.html', {
        'page_obj': page_obj,
        'total_products': products.count(),
    })


# ================= SHOP DETAIL =================
def shop_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop_detail.html', {
        'product': product
    })


# ================= CART =================
def cart(request):
    return render(request, 'cart.html')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity', 1))

    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity

    request.session['cart'] = cart
    return redirect('shop_detail', pk=product_id)