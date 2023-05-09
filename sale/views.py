from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Item
from Users.decorators import vendor_check,customer_check

@login_required(login_url='login')
@vendor_check
def dashboard(request):
    return render(request, 'Users/dashboard.html')
                  

# @login_required(login_url='login')
# def add_item(request):
#     if request.method == 'POST':
#         # process form data and create new item
#     else:
#         # display form for adding new item
#     return render(request, 'vendor/add_item.html')

# @login_required(login_url='/login/')
# def delete_item(request, item_id):
#     item = get_object_or_404(Item, pk=item_id, vendor=request.user.vendor)
#     # delete the item
#     return render(request, 'vendor/delete_item.html')

# @login_required(login_url='/login/')
# def vendor_profile(request):
#     items = request.user.vendor.items.all()
#     # display vendor profile page with list of items
#     return render(request, 'vendor/vendor_profile.html', {'items': items})
