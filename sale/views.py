from django.shortcuts import render,redirect
from django.urls import reverse,reverse_lazy
from .models import Item
from Users.decorators import vendor_check,customer_check
from django.views.generic import CreateView,DeleteView,UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages


class VendorCheckMixin(UserPassesTestMixin):
    def test_func(self):
        item = self.get_object()
        return self.request.user.is_authenticated and item.vendor == self.request.user.vendor
    
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
    context={'items':Item.objects.filter(vendor=request.user.id)}
    return render(request,'sale/vendor_items.html',context=context)

@customer_check
def home(request):
    context = {'items': Item.objects.order_by('-item_orders')}
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
    fields = ['item_title', 'item_price', 'item_description', 'item_image', 'item_stock']
    template_name_suffix = '_update'

    def get_success_url(self):
        return reverse('add-item')

@method_decorator(vendor_check,name='dispatch')
class DeleteItem(VendorCheckMixin,DeleteView):
    model = Item
    success_url = reverse_lazy('add-item')
    template_name_suffix = '_delete'




