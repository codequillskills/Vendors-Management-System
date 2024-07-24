from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Vendor, Product

# Create your views here.
@login_required
@csrf_protect
def dashboard(request):
    vendors = Vendor.objects.filter(user=request.user)
    products = Product.objects.filter(vendor__user=request.user)
    context = {
        'vendors': vendors,
        'products': products,
    }
    return render(request, 'dashboard.html', context)

@login_required
def delete_vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id, user=request.user)
    vendor.delete()
    return redirect('dashboard')

@login_required
@csrf_protect
def add(request):
    if request.method == 'POST':
        # Vendor Details
        vendor_name = request.POST.get('vendorname')
        vendor_phone = request.POST.get('vendorphone')
        vendor_email = request.POST.get('vendoremail')
        vendor_role = request.POST.get('role')
        
        print(f"Name: {vendor_name}, Phone Number: {vendor_phone}, Email: {vendor_email}, Role: {vendor_role}")  # Debugging line
        
        # Product Details
        product_name = request.POST.get('productname')
        product_category = request.POST.get('productcategory')
        product_price = request.POST.get('productprice')
        product_quantity = request.POST.get('productquantity')
        product_description = request.POST.get('productdescription')

        # Create and save Vendor
        vendor = Vendor.objects.create(
            user=request.user,
            name=vendor_name,
            phone_number=vendor_phone,
            email=vendor_email,
            role=vendor_role,
        )

        # Create and save Product
        product = Product.objects.create(
            vendor=vendor,
            name=product_name,
            category=product_category,
            price=product_price,
            quantity=product_quantity,
            description=product_description,
        )

        return redirect('dashboard')

    return render(request, 'add.html')

@csrf_protect
def registerPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if password != repassword:
            return redirect('register')
        if User.objects.filter(username=username).exists():
            return redirect('register')
        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
        except Exception as e:
            return redirect('register')
    return render(request, 'register.html')

@csrf_protect
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
@csrf_protect
def logoutPage(request):
    logout(request)
    return redirect('login')