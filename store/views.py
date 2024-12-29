from urllib import request
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import *
from login.forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .forms import BillingForm
from django.core.mail import send_mail
from bloodDonation.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

# Create your views here.


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def UserHome(request):
    if request.user.is_authenticated:
        count = len(Carts.objects.filter(user=request.user))
    else:
        count = 0

    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)
    banner = Banner.objects.all()[0:3]

    # Fetch all products or filter by search query
    if request.method == "GET":
        st = request.GET.get('Search')
        if st:
            product_list = Product.objects.filter(name__icontains=st)
        else:
            product_list = Product.objects.all().order_by('?')

    # Set up pagination
    paginator = Paginator(product_list, 8)  # Adjust the number of items per page as needed
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        products = paginator.page(paginator.num_pages)

    return render(request, 'homepage/home.html', {
        'products': products,
        'banner': banner,
        'cats': category,
        'sub': subcategory,
        'count': count
    })



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Carts  # Assuming you have a Cart model

def update_cart_product_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('pid')
        quantity = request.POST.get('quantity')

        # Assuming you have a Cart model with a method to update product quantity
        cart_product = Carts.objects.get(product_id=product_id)
        cart_product.update_quantity(quantity)

        messages.success(request, 'Quantity updated successfully.')
        return redirect('your-cart-page-url')  # Redirect to your cart page after updating quantity
    else:
        # Handle GET requests or other cases
        # Redirect or render as needed
        pass

class Product_detail_view(DetailView):
    model = Product
    template_name = 'homepage/product.html'

    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super(Product_detail_view, self).get_context_data(**kwargs)
        product = self.get_object()
        context['similar'] = Product.objects.filter(category__name = product.category.name).exclude(id=product.id)
        return context




def AddCart(request):
    if request.user.is_authenticated:
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)
        cart = Carts(user=request.user, product =product )
        cart.save()
        return redirect('showcart')
    else:
        return redirect('login')



from django.shortcuts import redirect
from django.contrib import messages
from .models import Carts

def update_quantity(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))

        # Get the cart items matching the conditions
        cart_items = Carts.objects.filter(product_id=product_id, user=request.user)

        if cart_items.exists():
            # Iterate over each cart item and update its quantity
            for cart_item in cart_items:
                cart_item.quantity = quantity
                cart_item.save()
            messages.success(request, 'Quantities updated successfully')
        else:
            messages.error(request, 'Cart item not found.')

    return redirect('showcart')






def removecart(request):
    if request.method =="GET":
        product_id = request.GET['product_id']
        cart = Carts.objects.filter( Q(product=product_id) & Q(user=request.user))
        cart.delete()
        shipping_cost = 70
        amount = 0
        cart_product = [p for p in Carts.objects.all() if p.user == request.user]

        for p in cart_product:
            amount = amount + p.product.price
            totalamount = amount + shipping_cost


        data={
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)




def products_by_category(request, category_id):
    if request.user.is_authenticated:
        count= len(Carts.objects.filter(user= request.user))
    else:
        count= 0
    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'homepage/categoryproduct.html', {'category': category, 'product': products, 'count':count,  'cats': category,
                                                      'sub': subcategory})

def showcart(request):
    if request.user.is_authenticated:
        count = Carts.objects.filter(user=request.user).count()
    else:
        count = 0

    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)

    if request.user.is_authenticated:
        cart = Carts.objects.filter(user=request.user)
        shipping_cost = 150
        totalamount = 0

        # Calculate total amount for all products in the cart
        for cart_item in cart:
            cart_item.amount = cart_item.quantity * cart_item.product.price
            totalamount += cart_item.amount



        return render(request, 'homepage/cart.html', {'carts': cart,
                                                      'shipping_cost': shipping_cost,
                                                      'totalamount': totalamount,
                                                      'cats': category,
                                                      'sub': subcategory,
                                                      'count': count})
    else:
        return render(request, 'homepage/cart.html', {'cats': category, 'sub': subcategory, 'count': count})

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Category, Carts, Orders, Product
from .forms import BillingForm

@login_required
def checkout(request):
    if request.user.is_authenticated:
        count = len(Carts.objects.filter(user=request.user))
    # Retrieve necessary data
    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)
    shipping_cost = 150  # Setting a different shipping cost as per the new logic
    totalamount = 0

    # Ensure the user is authenticated
    if request.user.is_authenticated:
        cart_products = Carts.objects.filter(user=request.user)

        # Calculate total amount for all products in the cart
        for cart_item in cart_products:
            cart_item.amount = cart_item.quantity * cart_item.product.price
            totalamount += cart_item.amount

        totalamount += shipping_cost  # Add shipping cost to the total amount

    # Handle POST request with form submission
    if request.method == 'POST':
        fm = BillingForm(request.POST)
        if fm.is_valid():
            billing_details = fm.save()
            orders = []
            for cart_item in cart_products:
                order = Orders.objects.create(
                    user=request.user,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    order=billing_details
                )
                orders.append(order)

            # Send email to admin about new orders
            subject = 'New orders placed'
            message = render_to_string('dashboard/orders_email.html', {'orders': orders})
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['mpias3721@gmail.com']
            send_mail(subject, '', from_email, recipient_list, html_message=message)

            # Clear the user's cart
            cart_products.delete()

            return redirect('orders')
    else:
        fm = BillingForm()

    # Render the checkout page with context data
    context = {
        'carts': cart_products,
        'shipping_cost': shipping_cost,
        'totalamount': totalamount,
        'amount': totalamount - shipping_cost,  # Calculate amount without shipping cost
        'form': fm,
        'cats': category,
        'sub': subcategory,
        'count': count ,
    }
    return render(request, 'homepage/checkout.html', context)

from django.shortcuts import render
from .models import Category, Orders
from django.contrib.auth.decorators import login_required

@login_required
def orders(request):
    if request.user.is_authenticated:
        count = 0
    # Retrieve necessary data
    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)
    orders = Orders.objects.filter(user=request.user)
    shipping_cost = 150
    totalamount = 0
    # Pass the data to the template
    return render(request, 'dashboard/Orders.html', {
        'orders': orders,
        'total': totalamount,
        'shipping_cost': shipping_cost,
        'cats': category,
        'sub': subcategory,
        'count': count ,

    })

def category(request):
    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)
    return render(request, 'base file/base.html', {'cats': category, 'sub': subcategory })

def about(request):
    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)
    map = "khulna"
    return render(request, 'homepage/about.html',{'cats': category, 'sub': subcategory, 'map': map})
def cart(request):
    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)
    return render(request, 'homepage/cart.html',{'cats': category, 'sub': subcategory,})

def blogs(request):
    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)
    return render(request, 'homepage/blog.html',{'cats': category, 'sub': subcategory,})

def contact(request):
    category = Category.objects.filter(parent=None)
    subcategory = Category.objects.exclude(parent=None)

    return render(request, 'homepage/contact.html',{'cats': category,'sub': subcategory,})

