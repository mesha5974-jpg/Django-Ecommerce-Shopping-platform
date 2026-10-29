from decimal import Decimal
from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib import messages
from django.views import View
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import RegistrationForm,LoginForm,ProductAddForm,OrderForm
from .models import Category,Product,OrderItem,Order
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.
class Homeview(View):
    def get(self,request):
        products = Product.objects.all()
        categories = Category.objects.all()
        context = {
            'products': products,
            'categories': categories
        }
        return render(request,"store/product_list.html",context)


class RegistrationView(View):
    def get(self,request):
        form = RegistrationForm()
        return render(request,"registration/register.html",{'form':form})

    def post(self,request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("home")
        return render(request,"registration/register.html",{"form":form})

class LoginView(View):
    def get(self,request):
        form = LoginForm()
        return render(request,"registration/login.html",{"form":form})
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user_obj = User.objects.filter(
            email__iexact=email
            ).first()
            if user_obj is not None:
               user = authenticate(request,username=user_obj.username,password=password)
            
               if user is not None:
                login(request,user)
                return redirect("product_list")
               
            messages.error(request,"Email or Password is Invalid")
        return render(request,"registration/login.html",{"form":form})

class LogoutView(View):
    def post(self,request):
        logout(request)
        return redirect("product_list")

class ProductListView(ListView):
    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(is_available=True).order_by('?')

class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"
    context_object_name ="product"
            
class CategoryView(View):
    def get(self,request,slug):
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category = category,is_available=True)
        return render (request,"store/product_list.html",{'category':category,'products':products})

class ProductAddView(LoginRequiredMixin,UserPassesTestMixin,CreateView):
    login_url = "/login/"
    model = Product
    form_class = ProductAddForm
    template_name = "store/add_product.html"
    success_url = reverse_lazy("product_list")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        category_name = form.cleaned_data['category'].strip()
        category_slug = slugify(category_name)
        if not category_slug:
            form.add_error("category","Please enter slug")
            return self.form_invalid(form)

        category,create = Category.objects.get_or_create(slug = category_slug, defaults={"name": category_name})
        form.instance.category = category
        return super().form_valid(form)

class ProductEditView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = "/login/"
    model = Product
    form_class = ProductAddForm
    template_name = "store/add_product.html"
    success_url = reverse_lazy("product_list")

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context
    
    def get_initial(self):
        initial =  super().get_initial()
        initial["category"] = self.object.category.name
        return initial
    
    def form_valid(self, form):
        category_name = form.cleaned_data["category"].strip()
        category_slug = slugify(category_name)

        if not category_slug:
            form.add_error("category","please enter category..")
            return self.form_invalid(form)
        
        category,create = Category.objects.get_or_create(slug=category_slug,defaults={"name":category_name})
        form.instance.category = category
        return super().form_valid(form)

class ProductDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = "/login/"
    model = Product
    success_url = reverse_lazy("product_list")
    def test_func(self):
        return self.request.user.is_staff

class CartAddView(View):
    def post(self,request,pk):
        product = get_object_or_404(Product,pk=pk,is_available = True)
        cart = request.session.get("cart",{})

        product_id = str(pk)
        current_quantity = int(cart.get(product_id ,0))

        if current_quantity + 1 > product.stock:
            messages.error(request,f'{product.name} is out of stock..')
            return redirect("product_list")
        
        quantity = current_quantity+1
        cart[product_id] = quantity
        request.session["cart"] = cart
        request.session.modified = True
        messages.success(request,f'{product.name} is added to cart!!')
        return redirect("product_list")
    
class CartView(View):
    def get(self,request):
        cart = request.session.get("cart",{})
        total = Decimal("0.00")
        cart_items = []

        for pk,quantity in cart.items():
            product = Product.objects.filter(pk=pk,is_available=True).first()
            if product is None:
                continue
            quantity = int(quantity)
            subtotal = product.price * quantity
            total += subtotal
            cart_items.append(
                {'product':product,
                 'quantity':quantity,
                 'subtotal' : subtotal,
                 }
            )
        return render(request,"cart/detail.html",{'cart_items':cart_items,'total':total})

class CartUpdateView(View):
  
  def post(self, request, pk):
    cart = request.session.get("cart", {})
    product_id = str(pk)

    product = get_object_or_404(
        Product, pk=pk, is_available=True
    )

    if product_id not in cart:
        messages.error(request, "Product is not in cart.")
        return redirect("cart")

    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        messages.error(request, "Invalid quantity.")
        return redirect("cart")

    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect("cart")

    if quantity > product.stock:
        messages.error(request, "Quantity exceeds available stock.")
        return redirect("cart")

    cart[product_id] = quantity
    request.session["cart"] = cart
    request.session.modified = True

    messages.success(request, "Cart quantity updated!")
    return redirect("cart")

class CartRemoveView(View):
    def post(self,request,pk):
        cart = request.session.get("cart",{})
        product_id = str(pk)
        cart.pop(product_id,None)
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request,"Product is remove!")

        return redirect('cart')

class CartClearView(View):
    def post(self,request):
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request,"Your Cart is Empty!")
        return redirect('cart')

class CheckOutView(LoginRequiredMixin, View):
    login_url = '/login/'   

    def get(self,request):
            cart_items = []
            total_amount = Decimal("0.00")
            form = OrderForm()
            cart = request.session.get('cart',{})
            if not cart:
                messages.error(request,"Your cart is Empty!!")
                return redirect('cart')
            
            for product_id,quantity in cart.items():
                
                try:
                  product = Product.objects.get(pk=int(product_id),is_available=True)
                  quantity = int(quantity)

                except (ValueError,TypeError,Product.DoesNotExist):
                    messages.error(request,f"Product is not available..")
                    return redirect('cart')

                if quantity > product.stock or quantity < 1:
                    messages.error(request,f'Product is out of stock!')
                    return redirect('cart')
                
                subtotal = product.price * quantity
                cart_items.append({"product":product,"quantity":quantity,"total_price":subtotal})
                total_amount +=subtotal

            return render(request,"orders/checkout.html",{'cart':cart,'form':form,"cart_items":cart_items,"total_amount":total_amount})
    

    def post(self, request):
        form = OrderForm(request.POST)
        cart = request.session.get("cart", {})

        if not cart:
            messages.error(request, "Your cart is empty!")
            return redirect("cart")

        if not form.is_valid():
            return render(request, "orders/checkout.html", {
                "cart": cart,
                "cart_items": [],
                "total_amount": Decimal("0.00"),
                "form": form,
            })

        if form.cleaned_data.get("payment") == "Card":
            form.add_error(
                "payment",
                "Online card payment is not available yet. "
                "Please select Cash on Delivery."
            )
            return render(request, "orders/checkout.html", {
                "cart": cart,
                "cart_items": [],
                "total_amount": Decimal("0.00"),
                "form": form,
            })

        cart_items = []
        total_amount = Decimal("0.00")

        try:
            with transaction.atomic():
                # Lock and validate every product before creating the order.
                for product_id, quantity in cart.items():
                    product = Product.objects.select_for_update().get(
                        pk=int(product_id),
                        is_available=True,
                    )
                    quantity = int(quantity)

                    if quantity < 1 or quantity > product.stock:
                        messages.error(
                            request,
                            f"Insufficient stock for {product.name}!"
                        )
                        return redirect("cart")

                    cart_items.append((product, quantity))
                    total_amount += product.price * quantity

                order = form.save(commit=False)
                order.user = request.user
                order.total_amount = total_amount
                order.save()

                for product, quantity in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        price=product.price,
                        quantity=quantity,
                    )

                    product.stock -= quantity
                    product.save(update_fields=["stock"])

        except (ValueError, TypeError, Product.DoesNotExist):
            messages.error(
                request,
                "A product is invalid or no longer available."
            )
            return redirect("cart")

        request.session["cart"] = {}
        request.session.modified = True

        messages.success(request, "Your order has been placed!")
        return redirect("order_success", pk=order.pk)

        
class OrderHistoryView(LoginRequiredMixin,ListView):
    model = Order
    login_url = '/login/'   
    template_name = "orders/order_history.html"
    context_object_name = "orders"
    def get_queryset(self):
       return  Order.objects.filter(user = self.request.user).order_by('created_at')

class OrderDetailView(LoginRequiredMixin,DetailView):
    model = Order
    login_url = '/login/'   
    template_name = "orders/order_detail.html"
    context_object_name = "order"
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

from django.core.mail import send_mail

class EmailConfirmationView(UserPassesTestMixin,View):

    def test_func(self):
        return self.request.user.is_staff
    
    def get(self,request):
        orders = Order.objects.all()
        return render(request,"admin.html",{"orders":orders,"status_choices": Order.STATUS_CHOICES})
    
    def post(self, request):
        order_id = request.POST.get("order_id")
        new_status = request.POST.get("status")

        order = get_object_or_404(Order, pk=order_id)

        valid_statuses = dict(Order.STATUS_CHOICES)

        if new_status not in valid_statuses:
            messages.error(request, "Invalid order status.")
            return redirect("admin_confirm")

        old_status = order.status

        order.status = new_status
        order.save(update_fields=["status"])

        if old_status != "confirmed" and new_status == "confirmed":
            if order.user.email:
                    subject = f"Order Confirmation - Order #{order.pk}"
                    product_details =""
                    for item in order.items.all():
                        product_details +=(
                        f'{item.product.name} | '
                        f'Quantity: {item.quantity} | '
                        f'Price: {item.price} | '
                        f'Total: {item.subtotal}')

                    message = (
                        f'Hello! {order.full_name}\n\n'
                        f'Thank you for placing your order!!\n\n'
                        f'Order Number {order.pk}\n'
                        f'Products \n {product_details}\n'
                        f'Total: {order.total_amount}\n\n'
                        f'Delivery Address: {order.address} , {order.city}\n'
                        f"Phone: {order.phone}\n\n"
                        f'Thank you for shopping with us!'
                    )
                    send_mail(
                        subject,message,settings.DEFAULT_FROM_EMAIL,
                         [order.user.email],fail_silently=False
                    )
        messages.success(request, "Confirmation emails processed...")
        return redirect("admin_confirm")

class OrderSuccessView(LoginRequiredMixin,DetailView):
    model = Order
    login_url = '/login/'   
    template_name = "orders/order_success.html"
    context_object_name = "order"
    def get_queryset(self):
        order = Order.objects.filter(user = self.request.user)
        return order