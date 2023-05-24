from django.shortcuts import render,redirect,get_object_or_404
from .models import Cart,CartItem,Order,OrderItem,Wishlist
from sale.models import Item
from Users.decorators import vendor_check,customer_check
from django.contrib import messages
from .forms import AddToCartForm
from django.db import transaction
from django.db.models import F
from django.core.mail import send_mail

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
    return render(request, 'orders/add_to_cart.html', context=context)

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
    
    return render(request, 'orders/remove_from_cart.html', context)

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

    return render(request, 'orders/cart_details.html', context=context)


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
            
        send_mail(subject=f'EurekaMart: New Order Recieved!', from_email='f20221270@pilani.bits-pilani.ac.in',
                   message=f'You have recieved an order from {request.user.customer} on EurekaMart'
                   , recipient_list=[cart_item.item.vendor.user.email])

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
    return render(request, 'orders/customer_order_details.html', context=context)


@customer_check
def customer_order_history(request):
    orders = Order.objects.filter(customer=request.user.customer).order_by('order_date')

    context = {
        'orders': orders,
    }
    return render(request, 'orders/customer_order_history.html', context=context)

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
    return render(request, 'orders/vendor_order_details.html', context=context)

@vendor_check
def vendor_order_history(request):
    orders = Order.objects.filter(order_items__item__vendor=request.user.vendor).distinct().order_by('order_date')

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
    return render(request, 'orders/vendor_order_history.html', context=context)

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
    return render(request, 'orders/wishlist.html', context=context)

