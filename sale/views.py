from django.shortcuts import render
from django.urls import reverse
from .models import Item
from Users.decorators import vendor_check,customer_check
from django.views.generic import CreateView
from django.utils.decorators import method_decorator


@vendor_check
def dashboard(request):
    return render(request, 'Users/dashboard.html')

@customer_check
def home(request):
    context = {'items': Item.objects.all()}
    return render(request, 'Users/home.html', context=context)


@method_decorator(vendor_check,name='dispatch')
class AddItem(CreateView):
    model=Item
    fields=['item_title','item_price','item_description','item_image','item_stock']
    
    def form_valid(self, form):
        form.instance.vendor = self.request.user.vendor
        return super().form_valid(form)

    def get_success_url(self):
       return reverse('add-item')
    


