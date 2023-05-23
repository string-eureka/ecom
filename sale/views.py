from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse,reverse_lazy
from .models import Item,Cart,CartItem,Order,OrderItem,Wishlist,Review
from Users.decorators import vendor_check,customer_check
from django.views.generic import CreateView,DeleteView,UpdateView,FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddMoneyForm,AddToCartForm,ReviewForm
from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.db.models import F,Q,Avg,ExpressionWrapper,DecimalField


class VendorCheckMixin(UserPassesTestMixin): 
    def test_func(self):
        item = self.get_object()
        return self.request.user.is_authenticated and item.vendor == self.request.user.vendor and not self.request.user.is_superuser 
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.warning(self.request, 'You are not authorized to perform this action.')
            return redirect('login-redirect')  
        return redirect('login')

class CustomerCheckMixin(UserPassesTestMixin):
    def test_func(self):
        item = self.get_object()
        return self.request.user.is_authenticated and item.customer == self.request.user.customer and not self.request.user.is_superuser 
    
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            messages.warning(self.request, 'You are not authorized to perform this action.')
            return redirect('login-redirect')  
        return redirect('login')

@vendor_check
def dashboard(request):
    low_stock_items = Item.objects.filter(vendor=request.user.id, item_stock__lt=3)
    
    context = {
        'low_stock_items': low_stock_items,
    }

    return render(request, 'Users/dashboard.html', context=context)

    

@vendor_check
def vendor_items(request):
    items = Item.objects.filter(vendor=request.user.id)
    context = {'items': items}
    return render(request, 'sale/vendor_items.html', context=context)


@customer_check
def home(request):
    sort_by = request.GET.get('sort_by')
    items = Item.objects.all()

    if sort_by == 'orders':
        items = items.order_by('-item_orders')
    elif sort_by == 'price_low_high':
        items = items.annotate(
            calculated_selling_price=ExpressionWrapper(
                F('item_price') - ((F('item_price') * F('item_discount')) / 100),
                output_field=DecimalField()
            )
        ).order_by('calculated_selling_price')
    elif sort_by == 'price_high_low':
        items = items.annotate(
            calculated_selling_price=ExpressionWrapper(
                F('item_price') - ((F('item_price') * F('item_discount')) / 100),
                output_field=DecimalField()
            )
        ).order_by('-calculated_selling_price')
    elif sort_by == 'average_rating':
        items = items.annotate(avg_rating=Avg('item_reviews__rating')).order_by('-avg_rating')

    context = {'items': items}
    return render(request, 'Users/home.html', context=context)


@login_required
def wallet(request):
    return render(request,'sale/wallet.html')

@customer_check
def random_item(request):
    try:
        random_item = Item.objects.order_by('?').first()  
        if random_item:
            return redirect('item-detail', item_id=random_item.id)
    except Item.DoesNotExist:
        messages.warning(request,'No Items have been added yet.')
    return redirect('home') 

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
        return reverse('vendor-items')
    

@method_decorator(vendor_check,name='dispatch')
class EditItem(VendorCheckMixin,UpdateView):
    model = Item
    fields = ['item_title', 'item_price', 'item_description', 'item_image', 'item_stock','item_discount']
    template_name_suffix = '_update'

    def get_success_url(self):
        messages.success(self.request,'Item updated successfully')
        return reverse('vendor-items')


@method_decorator(vendor_check,name='dispatch')
class DeleteItem(VendorCheckMixin,DeleteView):
    model = Item
    template_name_suffix = '_delete'

    def get_success_url(self):
        messages.success(self.request,'Item deleted successfully')
        return reverse('vendor-items')


@method_decorator(customer_check, name='dispatch')
class AddMoney(FormView):
    form_class = AddMoneyForm
    template_name = 'sale/add_money.html'

    def form_valid(self, form):
        balance = form.cleaned_data['balance']
        user = self.request.user
        try:
            new_balance = user.balance + Decimal(balance)
            if new_balance < 0 or new_balance > 10 ** 17:
                raise InvalidOperation("Invalid balance")
            user.balance = new_balance
            user.save()
            messages.success(self.request, f'${balance} added to your account!')
            return super().form_valid(form)
        except InvalidOperation as e:
            form.add_error('balance', str(e))
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('wallet')


@login_required
def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    reviews = item.item_reviews.all()

    if request.user.user_type == 'CS':
        review_exists = Review.objects.filter(item=item, owner=request.user.customer).exists()
        has_ordered = Order.objects.filter(Q(customer=request.user.customer) & Q(order_items__item=item)).exists()
    else:
        review_exists=False
        has_ordered=False
    context = {
        'item': item,
        'reviews': reviews,
        'has_ordered':has_ordered,
        'review_exists':review_exists,
    }
    return render(request, 'sale/item_detail.html', context)

@customer_check
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
            return redirect('cart-details')
    else:
        initial_quantity = cart_item.quantity if cart_item else 0
        form = AddToCartForm(initial={'quantity': initial_quantity})
    
    context = {
        'item': item,
        'form': form,
        'current_quantity': cart_item.quantity if cart_item else 0,  
        }
    return render(request, 'sale/add_to_cart.html', context=context)

@customer_check
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    
    if request.method == 'POST':
        cart_item.delete()
        messages.success(request, f'{cart_item.item.item_title} removed from cart.')
        return redirect('cart-details')
    
    context = {
        'cart_item': cart_item
    }
    
    return render(request, 'sale/remove_from_cart.html', context)

@customer_check
def cart_details(request):
    cart,created = Cart.objects.get_or_create(owner=request.user.customer)
    cart_items = cart.cart_items.all()
    for cart_item in cart_items:
        cart_item.total_iprice = cart_item.item.selling_price * cart_item.quantity
        if cart_item.item.item_stock < cart_item.quantity:
            cart_item.stock = 0
        else: 
            cart_item.stock = 1
        
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }

    return render(request, 'sale/cart_details.html', context=context)


@customer_check
@transaction.atomic

def create_order(request):
    cart = get_object_or_404(Cart, owner=request.user.customer)
    total_bill = cart.calculate_bill
    saving=cart.savings

    if request.user.balance < total_bill:
        messages.warning(request, "Insufficient balance to place the order.")
        return redirect('cart-details')
    if total_bill > 10 ** 10:
        messages.warning(request,'In line with government regulations, We are unable to process orders greater than $1000000000!')
        return redirect('cart-details')


    vendor_balances = {}

    for cart_item in cart.cart_items.all():
        if cart_item.item.item_stock < cart_item.quantity:
            messages.warning(request, f"Insufficient stock for {cart_item.item.item_title}.")
            return redirect('cart-details')

        vendor = cart_item.item.vendor.user
        vendor_balances[vendor] = vendor_balances.get(vendor, 0) + (cart_item.quantity * cart_item.item.selling_price)

        cart_item.item.item_stock -= cart_item.quantity
        cart_item.item.item_orders += cart_item.quantity
        cart_item.item.save()

    order = Order.objects.create(customer=request.user.customer, total_bill=total_bill,saving=saving)
    order_items = []

    for cart_item in cart.cart_items.all():
        order_item = OrderItem(
            order=order,
            item=cart_item.item,
            quantity=cart_item.quantity,
            item_price=cart_item.item.selling_price,
            item_title=cart_item.item.item_title
        )
        order_items.append(order_item)

    OrderItem.objects.bulk_create(order_items)

    for vendor, balance_change in vendor_balances.items():
        vendor.balance = F('balance') + balance_change
        vendor.save()

    request.user.balance -= total_bill
    request.user.save()

    cart.cart_items.all().delete()
    messages.success(request, "Order placed successfully.")
    return redirect('customer-order-details', order.pk)

@customer_check
def customer_order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer=request.user.customer)
    order_items = order.order_items.all()
    for order_item in order_items:
        order_item.total_iprice = order_item.item_price * order_item.quantity
    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'sale/customer_order_details.html', context=context)


@customer_check
def customer_order_history(request):
    orders = Order.objects.filter(customer=request.user.customer).order_by('-order_date')

    context = {
        'orders': orders,
    }
    return render(request, 'sale/customer_order_history.html', context=context)

@vendor_check
def vendor_order_details(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order_items = order.order_items.filter(item__vendor=request.user.vendor)
    total_earned = sum(item.item_price * item.quantity for item in order_items)
    for order_item in order_items:
        order_item.total_iprice = order_item.item_price * order_item.quantity

    context = {
        'order': order,
        'order_items': order_items,
        'total_earned': total_earned,
    }
    return render(request, 'sale/vendor_order_details.html', context=context)

@vendor_check
def vendor_order_history(request):
    orders = Order.objects.filter(order_items__item__vendor=request.user.vendor).distinct().order_by('-order_date')

    order_data = []
    for order in orders:
        order_items = order.order_items.filter(item__vendor=request.user.vendor)
        total_earned = sum(item.item_price * item.quantity for item in order_items)
        order_data.append({
            'order': order,
            'total_earned': total_earned,
        })

    context = {
        'order_data': order_data,
    }
    return render(request, 'sale/vendor_order_history.html', context=context)

@customer_check
def add_to_wishlist(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    wishlist, created = Wishlist.objects.get_or_create(owner=request.user.customer)
    wishlist.items.add(item)
    messages.success(request, f"{item.item_title} added to your wishlist.")
    return redirect('wishlist')

@customer_check
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    wishlist = get_object_or_404(Wishlist, owner=request.user.customer)
    wishlist.items.remove(item)
    messages.success(request, f"{item.item_title} removed from your wishlist.")
    return redirect('wishlist')

@customer_check
def wishlist(request):
    wishlist,created = Wishlist.objects.get_or_create(owner=request.user.customer)
    items = wishlist.items.all()
    context = {'items': items}
    return render(request, 'sale/wishlist.html', context=context)

@customer_check
def leave_review(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    review_exists = Review.objects.filter(item=item, owner=request.user.customer).exists()
    
    if review_exists:
        messages.warning(request, "You have already reviewed this item.")
        return redirect('item-detail', item_id=item.id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.owner = request.user.customer
            review.save()
            messages.success(request, "Review submitted successfully.")
            return redirect('item-detail', item_id=item.id)
    else:
        form = ReviewForm()

    context = {
        'item': item,
        'form': form,
    }
    return render(request, 'sale/leave_review.html', context)
