from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Item,Review
from orders.models import Order
from Users.decorators import vendor_check,customer_check
from django.views.generic import CreateView,DeleteView,UpdateView,FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AddMoneyForm,ReviewForm
from decimal import Decimal, InvalidOperation
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

@vendor_check
def dashboard(request):
    low_stock_items = Item.objects.filter(vendor=request.user.id, item_stock__lt=4)
    
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
    random_item = Item.objects.order_by('?').first()  
    if random_item:
        return redirect('item-detail', item_id=random_item.id)
    else:
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
