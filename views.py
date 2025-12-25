from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from datetime import date
from .models import Medicine,Customer, Sale
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache



def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('/dashboard/')
    return render(request, 'store/login.html')

@login_required
@never_cache
def dashboard(request):
    return render(request, 'store/dashboard.html', {
'medicines': Medicine.objects.count(),
'sales': Sale.objects.count()
})

@login_required
def add_medicine(request):
    if request.method == 'POST':
        Medicine.objects.create(
        name=request.POST['name'],
        cause=request.POST['cause'],
        batch_no=request.POST['batch'],
        company=request.POST['company'],
        expiry_date=request.POST['expiry'],
        price=request.POST['price'],
        quantity=request.POST['quantity'],
        )
        return redirect('/medicines/')
    return render(request, 'store/add_medicine.html')

@login_required
@never_cache
def medicine_list(request):
    query = request.GET.get('q')

    if query:
        medicines = Medicine.objects.filter(
            Q(name__icontains=query) |
            Q(cause__icontains=query) |
            Q(company__icontains=query) |
            Q(batch_no__icontains=query)
        )
    else:
        medicines = Medicine.objects.all()

    return render(request, 'store/medicine_list.html', {
        'medicines': medicines,
        'today': date.today(),
        'query': query
    })

@login_required
@never_cache
def edit_medicine(request, id):
    med = get_object_or_404(Medicine, id=id)
    if request.method == 'POST':
        med.name = request.POST['name']
        med.quantity = request.POST['quantity']
        med.save()
        return redirect('/medicines/')
    return render(request, 'store/add_medicine.html', {'med': med})

def delete_medicine(request, id):
    Medicine.objects.filter(id=id).delete()
    return redirect('/medicines/')

@login_required
@never_cache
def sell_medicine(request):
    medicines = Medicine.objects.all()
    if request.method == 'POST':
        med = Medicine.objects.get(id=request.POST['medicine'])
        qty = int(request.POST['quantity'])
        if med.quantity >= qty:
            cust = Customer.objects.create(
            name=request.POST['customer'],
            mobile=request.POST['mobile']
            )
            Sale.objects.create(
            medicine=med,
            customer=cust,
            quantity_sold=qty
            )
            med.quantity -= qty
            med.save()
            return redirect('/sales/')
        else:
            messages.error(request,"invalid quantity")

    return render(request, 'store/sell_medicine.html', {'medicines': medicines})

@login_required
@never_cache
def sales(request):
    return render(request, 'store/sales.html', {
    'sales': Sale.objects.all()
    })