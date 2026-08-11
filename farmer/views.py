from django.db.models import Sum,F
from .models import Product, Category, Order, OrderItem
from decimal import Decimal
from .models import FarmerProfile
from .forms import ProductForm
from .utils import generate_invoice
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import random
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignupForm

# ================= HOME =================
def index(request):

    # 🔹 Show ONLY 6 products in "Our Organic Products"
    products = Product.objects.all().order_by('-id')[:6]

    # 🔹 Best Seller products (you already have is_bestseller field)
    best_sellers = Product.objects.filter(is_bestseller=True).order_by('-id')[:4]

    # 🔹 Vegetables carousel (category name based)
    vegetables = Product.objects.filter(
        category__name__icontains='vegetable'
    ).order_by('-id')[:8]

    context = {
        'products': products,
        'best_sellers': best_sellers,
        'vegetables': vegetables,
    }

    return render(request, 'index.html', context)


# ================= SHOP =================



from django.db.models import Q, Count
from django.core.paginator import Paginator

def shop(request):
    sort = request.GET.get('sort')
    q = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    # 🔍 SEARCH (apple / banana)
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    # 💰 PRICE FILTER
    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # 🔃 SORTING
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    elif sort == 'newest':
        products = products.order_by('-id')
    else:
        products = products.order_by('-id')

    categories = Category.objects.annotate(
        product_count=Count('product')
    )

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'current_sort': sort,
        'selected_category': None,
    }
    return render(request, 'shop.html', context)




def shop_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    sort = request.GET.get('sort')
    q = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(category=category)

    # 🔍 SEARCH inside category
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

    # 💰 PRICE FILTER
    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    # 🔃 SORTING
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    elif sort == 'newest':
        products = products.order_by('-id')
    else:
        products = products.order_by('-id')

    categories = Category.objects.annotate(
        product_count=Count('product')
    )

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'current_sort': sort,
        'selected_category': category,
    }
    return render(request, 'shop.html', context)



# ================= CART =================
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for pid, item in cart.items():
        product = get_object_or_404(Product, id=pid)
        subtotal = item['price'] * item['quantity']
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': item['quantity'],
            'get_total_price': subtotal
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    pid = str(product.id)

    if pid in cart:
        cart[pid]['quantity'] += 1
    else:
        cart[pid] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url if product.image else ''
        }

    request.session['cart'] = cart

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'cart_count': len(cart)
        })

    return redirect('cart')



def increase_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        cart[pid]['quantity'] += 1
    request.session['cart'] = cart
    return redirect('cart')


def decrease_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        cart[pid]['quantity'] -= 1
        if cart[pid]['quantity'] <= 0:
            del cart[pid]
    request.session['cart'] = cart
    return redirect('cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)
    if pid in cart:
        del cart[pid]
    request.session['cart'] = cart
    return redirect('cart')


# ================= CHECKOUT =================
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0.00')

    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = item['quantity']
        price = product.price
        subtotal = price * quantity
        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def place_order(request):
    if request.method != "POST":
        return redirect('checkout')

    cart = request.session.get('cart', {})
    if not cart:
        return redirect('shop')

    payment_method = request.POST.get('payment_method')
    total = Decimal('0')

    # CREATE ORDER
    order = Order.objects.create(
        customer=request.user,
        total_amount=0,
        payment_method=payment_method,
        payment_status="PENDING"
    )

    # CREATE ORDER ITEMS
    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = int(item['quantity'])
        price = Decimal(item['price'])

        OrderItem.objects.create(
            order=order,
            product=product,
            farmer=product.farmer,
            price=price,
            cost_price=product.cost_price,
            quantity=quantity
        )

        total += price * quantity

    # UPDATE TOTAL (THIS WAS THE KEY ISSUE)
    order.total_amount = total
    order.save()

    # CLEAR CART
    request.session['cart'] = {}


    if payment_method == "COD":
        return redirect('order_success', order_id=order.id)
    else:
        return redirect('upi_payment', order_id=order.id)



@login_required
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    return render(request, 'order_success.html', {
        'order': order
    })




# ================= DASHBOARDS =================
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime

@login_required
def farmer_dashboard(request):
    if request.user.role != 'farmer':
        return redirect('customer_dashboard')

    farmer_profile, created = FarmerProfile.objects.get_or_create(
        user=request.user
    )

    # Products
    products = Product.objects.filter(farmer=request.user)
    total_products = products.count()

    # Orders
    order_items = OrderItem.objects.filter(farmer=request.user).select_related(
        'order', 'product'
    ).order_by('-order__created_at')

    total_orders = order_items.count()

    # Total earning
    total_earning = order_items.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0

    # Monthly earning
    now = datetime.now()
    monthly_earning = order_items.filter(
        order__created_at__year=now.year,
        order__created_at__month=now.month
    ).aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0

    # Total profit
    total_profit = order_items.aggregate(
        profit=Sum((F('price') - F('cost_price')) * F('quantity'))
    )['profit'] or 0

    context = {
        'farmer_profile': farmer_profile,
        'products': products,
        'order_items': order_items,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_earning': total_earning,
        'monthly_earning': monthly_earning,
        'total_profit': total_profit,
    }

    return render(request, 'farmer/farmer_dashboard.html', context)



@login_required
def farmer_orders(request):
    order_items = OrderItem.objects.filter(farmer=request.user)
    total_earning = order_items.aggregate(
        total=Sum('price')
    )['total'] or 0

    return render(request, 'farmer/farmer_orders.html', {
        'order_items': order_items,
        'total_earning': total_earning
    })


@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        return redirect('farmer_dashboard')

    return render(request, 'customer/customer_dashboard.html')




@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'order_history.html', {'orders': orders})


# ================= STATIC PAGES =================
def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')



@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()


            return redirect('farmer_dashboard')
        else:
            print(form.errors)
    else:
        form = ProductForm()

    return render(request, 'farmer/add_product.html', {'form': form})


@login_required
def edit_product(request, pk):
    product = Product.objects.get(pk=pk, farmer=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()


            return redirect('farmer_dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'farmer/add_product.html', {'form': form})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, farmer=request.user)

    product.delete()


    return redirect('farmer_dashboard')



def shop_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'shop_detail.html', {
        'product': product
    })




def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    # Optional safety check
    if order.payment_status != 'PAID':
        return HttpResponse("Invoice available after payment only.")

    return generate_invoice(order)



@login_required
def upi_payment(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user,
        payment_method="UPI"
    )

    # If already paid, prevent re-payment
    if order.payment_status == "PAID":
        return redirect("order_success", order_id=order.id)

    if request.method == "POST":
        upi_app = request.POST.get("upi_app")  # GPay or PhonePe

        # DEMO PAYMENT SUCCESS
        order.payment_status = "PAID"
        order.save()

        return redirect("order_success", order_id=order.id)

    return render(request, "upi_payment.html", {"order": order})


@login_required
def upi_app_payment(request, order_id, app):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user,
        payment_method="UPI"
    )

    if order.payment_status == "PAID":
        return redirect("order_success", order_id=order.id)

    if request.method == "POST":
        return redirect("upi_processing", order_id=order.id)

    return render(request, "upi_app_payment.html", {
        "order": order,
        "app": app
    })



@login_required
def upi_processing(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    # ❌ Prevent double payment
    if order.payment_status == "PAID":
        return redirect("order_success", order_id=order.id)

    # 🎲 RANDOM SUCCESS / FAILURE
    success = random.choice([True, True, False])  # 66% success

    if success:
        order.payment_status = "PAID"

        # 🔢 FAKE UPI REFERENCE NUMBER
        order.upi_reference = (
            f"UPI{order.id}{timezone.now().strftime('%H%M%S')}"
        )

    else:
        order.payment_status = "FAILED"

    order.save()

    return render(
        request,
        "upi_processing.html",
        {"order": order}
    )

def cart_count(request):
    cart = request.session.get('cart', {})
    return {
        'cart_count': len(cart)
    }

from .forms import SignupForm   # ADD THIS IMPORT

from .forms import SignupForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import SignupForm
from .models import FarmerProfile


def auth_page(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "signup":
            form = SignupForm(request.POST)
            # 🛑 CRITICAL: Check if valid BEFORE doing anything else
            if form.is_valid():
                data = form.cleaned_data

                # Check if username exists
                if User.objects.filter(username=data['username']).exists():
                    form.add_error('username', 'Username already taken.')
                    return render(request, "signup.html", {"form": form, "active_tab": "signup"})

                # Create User
                user = User.objects.create_user(
                    username=data['username'],
                    email=data['email'],
                    password=data['password']
                )

                # Create FarmerProfile if role is farmer
                if data['role'] == 'farmer':
                    FarmerProfile.objects.create(
                        user=user,
                        phone=data['phone']
                    )

                login(request, user)
                return redirect("index")

            else:
                # 🔴 Show Red Errors: Re-render the page with the invalid form
                return render(request, "signup.html", {
                    "form": form,
                    "active_tab": "signup"
                })

        elif form_type == "login":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("index")
            else:
                return render(request, "signup.html", {
                    "form_errors": {"login": ["Invalid username or password."]},
                    "active_tab": "login"
                })

    return render(request, "signup.html", {"form": SignupForm()})