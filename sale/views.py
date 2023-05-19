from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from .models import Item,Cart,CartItem,Order
from Users.decorators import vendor_check,customer_check
from django.views.generic import CreateView,DeleteView,UpdateView,FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddMoneyForm,AddToCartForm

class VendorCheckMixin(UserPassesTestMixin):
    def test_func(self):
        item = self.get_object()
        return self.request.user.is_authenticated and item.vendor == self.request.user.vendor
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.warning(self.request, 'You are not authorized to perform this action.')
            return redirect('login-redirect')  
        return redirect('login')

class CustomerCheckMixin(UserPassesTestMixin):
    def test_func(self):
        item = self.get_object()
        return self.request.user.is_authenticated and item.customer == self.request.user.customer
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.warning(self.request, 'You are not authorized to perform this action.')
            return redirect('login-redirect')  
        return redirect('login')

@vendor_check
def dashboard(request):
    return render(request, 'Users/dashboard.html')
    

@vendor_check
def vendor_items(request):
    items = Item.objects.filter(vendor=request.user.id)
    context = {'items': items}
    return render(request, 'sale/vendor_items.html', context=context)


@customer_check
def home(request):
    items=Item.objects.order_by('-item_orders')
    context = {'items': items}
    return render(request, 'Users/home.html', context=context)


@method_decorator(vendor_check,name='dispatch')
class AddItem(CreateView):
    model = Item
    fields = ['item_title', 'item_price', 'item_description', 'item_image', 'item_stock']

    def form_valid(self, form):
        form.instance.vendor = self.request.user.vendor
        response = super().form_valid(form)
        messages.success(self.request, 'Item added successfully')
        return response

    def get_success_url(self):
        return reverse('add-item')
    

@method_decorator(vendor_check,name='dispatch')
class EditItem(VendorCheckMixin,UpdateView):
    model = Item
    fields = ['item_title', 'item_price', 'item_description', 'item_image', 'item_stock','item_discount']
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse('vendor-items')


@method_decorator(vendor_check,name='dispatch')
class DeleteItem(VendorCheckMixin,DeleteView):
    model = Item
    template_name_suffix = '_delete'

    def get_success_url(self):
        return reverse('vendor-items')


@method_decorator(customer_check, name='dispatch')
class AddMoney(FormView):
    form_class = AddMoneyForm
    template_name = 'sale/add_money.html'

    def form_valid(self, form):
        amount = form.cleaned_data['balance']
        user = self.request.user
        user.balance += amount
        user.save()
        messages.success(self.request, f'${amount} added to your account!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile')

@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    context = {
        'item': item,
    }
    return render(request, 'sale/item_detail.html', context)


def add_to_cart(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    cart,created = Cart.objects.get_or_create(owner=request.user.customer)
    cart_item = CartItem.objects.filter(cart=cart, item=item).first()
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if cart_item:
                cart_item.quantity = quantity  
                cart_item.save()
                messages.success(request, f"The quantity of {item.item_title} in your cart has been updated.")
            else:
                CartItem.objects.create(cart=cart, item=item, quantity=quantity)
                messages.success(request, f"{quantity} {item.item_title} added to your cart.")
            return redirect('home')
    else:
        initial_quantity = cart_item.quantity if cart_item else 0
        form = AddToCartForm(initial={'quantity': initial_quantity})
    
    context = {
        'item': item,
        'form': form,
        'current_quantity': cart_item.quantity if cart_item else 0,  
        }
    return render(request, 'sale/add_to_cart.html', context=context)


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    if request.method == 'POST':
        cart_item.delete()
        return redirect('cart-details')
    context = {
        'cart_item': cart_item
    }
    messages.success(request,f'{cart_item.item.item_title} removed from cart.')
    return render(request, 'sale/cart_details.html', context)


def cart_details(request):
    cart = get_object_or_404(Cart, owner=request.user.customer)
    cart_items = cart.cart_items.all()
    saving=0
    for cart_item in cart_items:
        cart_item.total_iprice = cart_item.item.selling_price * cart_item.quantity
        saving+=(cart_item.item.item_price - cart_item.item.selling_price)
        
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'saving':saving,
    }

    return render(request, 'sale/cart_details.html', context=context)

