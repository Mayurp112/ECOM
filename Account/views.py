from tokenize import group
from django.shortcuts import get_object_or_404, render,redirect
from . import forms,models
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from .models import Customer, Orders, Product
from django.contrib.auth import authenticate
from django.views import View
from django.contrib.auth.models import User
from .forms import CustomerUserForm,CustomerForm
from django.contrib.auth.models import Group

from django.contrib.auth import authenticate,login,logout



# Create your views here.


def home_view(request):
    products=Product.objects.all()
    return render(request,'home.html',{'products':products})


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')



# Customer Signup View
class customer_signup_view(View):
    
    def get(self, request):
        userForm = CustomerUserForm()
        customerForm = CustomerForm()

        mydict = {'userForm': userForm, 'customerForm': customerForm}
        return render(request, 'customersignup.html', context=mydict)

    def post(self, request):
        userForm = CustomerUserForm(request.POST)
        customerForm = CustomerForm(request.POST, request.FILES)

        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()

            my_customer_group, created = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group.user_set.add(user)
            
            return HttpResponseRedirect('customerlogin')

        mydict = {'userForm': userForm, 'customerForm': customerForm}
        return render(request, 'customersignup.html', context=mydict)



class customer_login(View):
    def get(self,request):
        return render(request,'customerlogin.html')

    def post(self,request):
        if request.method=='POST':
            uname=request.POST.get('username')
            upass=request.POST.get('password')
            user=authenticate(request,username=uname,password=upass)
            print(user)
            print(uname,upass)
            if user is not None:
                login(request,user)
                return redirect(to=' ')
            else:
                messages.warning(request,f' Something Went Wrong While Login ')
                return redirect(to='customerlogin')







#_____ for checking user is customer
def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()



#_____ AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,CUSTOMER
def afterlogin_view(request):
    if is_customer(request.user):
        return redirect('customer-home')
    else:
        return redirect('profile-view')






@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    
    customercount=models.Customer.objects.all().count()
    productcount=models.Product.objects.all().count()
    ordercount=models.Orders.objects.all().count()

    
    mydict={
    'customercount':customercount,
    'productcount':productcount,
    'ordercount':ordercount,
    }
    return render(request,'admin_dashboard.html',context=mydict)

# admin view customer table

@login_required(login_url='customerlogin')
def customer_home_view(request):
    products=Product.objects.all()
    
    return render(request,request,'home.html',{'products':products})



class add_to_cart_view(View):
    def get(self, request, pk):
        products = models.Product.objects.all()

        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            counter = product_ids.split('|')
            product_count_in_cart = len(set(counter))
        else:
            product_count_in_cart = 1

        response = render(request, 'home.html', {'products': products, 'product_count_in_cart': product_count_in_cart})

        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            if product_ids == "":
                product_ids = str(pk)
            else:
                product_ids = product_ids + "|" + str(pk)
            response.set_cookie('product_ids', product_ids)
        else:
            response.set_cookie('product_ids', pk)

        product = get_object_or_404(models.Product, pk=pk)
        messages.info(request, f"{product.name} added to cart successfully")

        return response
    


class remove_from_cart_view(View):
    def get(self, request, pk):
        product_ids = request.COOKIES.get('product_ids', '')
        counter = product_ids.split('|') if product_ids else []
        product_count_in_cart = len(set(counter))

        total = 0
        if product_ids:
            product_id_in_cart = product_ids.split('|')
            product_id_in_cart = list(set(product_id_in_cart))
            product_id_in_cart.remove(str(pk))
            products = models.Product.objects.filter(id__in=product_id_in_cart)

            for p in products:
                total += p.price

            value = "|".join(product_id_in_cart)
            response = render(request, 'cart.html', {
                'products': products,
                'total': total,
                'product_count_in_cart': product_count_in_cart
            })

            if not value:
                response.delete_cookie('product_ids')
            response.set_cookie('product_ids', value)
            return response

    def post(self, request, pk):
        pass


class cart_view(View):
    def get(self, request):
        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            counter = product_ids.split('|')
            product_count_in_cart = len(set(counter))
        else:
            product_count_in_cart = 0

        products = None
        total = 0

        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            if product_ids != "":
                product_id_in_cart = product_ids.split('|')
                products = Product.objects.filter(id__in=product_id_in_cart)

                for p in products:
                    total += p.price

        return render(request, 'cart.html', {'products': products, 'total': total, 'product_count_in_cart': product_count_in_cart})

    def post(self):
        pass



@login_required(login_url='customerlogin')
def my_profile_view(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'my_profile.html',{'customer':customer})




class edit_profile_view(View):
    def get(self, request):
        customer = models.Customer.objects.get(user_id=request.user.id)
        user = models.User.objects.get(id=customer.user_id)
        userForm = forms.CustomerUserForm(instance=user)
        customerForm = forms.CustomerForm(instance=customer)
        mydict = {'userForm': userForm, 'customerForm': customerForm}
        return render(request, 'edit_profile.html', context=mydict)

    def post(self, request):
        customer = models.Customer.objects.get(user_id=request.user.id)
        user = models.User.objects.get(id=customer.user_id)
        userForm = forms.CustomerUserForm(request.POST, instance=user)
        customerForm = forms.CustomerForm(request.POST, request.FILES, instance=customer)
        mydict = {'userForm': userForm, 'customerForm': customerForm}

        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('my-profile')
        return render(request, 'edit_profile.html', context=mydict)
    
    

class customer_address_view(View):
    def get(self, request):
        product_in_cart = False
        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            if product_ids != "":
                product_in_cart = True

        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            counter = product_ids.split('|')
            product_count_in_cart = len(set(counter))
        else:
            product_count_in_cart = 0

        addressForm = forms.AddressForm()
        return render(request, 'customer_address.html', {
            'addressForm': addressForm,
            'product_in_cart': product_in_cart,
            'product_count_in_cart': product_count_in_cart
        })

    def post(self, request):
        addressForm = forms.AddressForm(request.POST)
        if addressForm.is_valid():
            email = addressForm.cleaned_data['Email']
            mobile = addressForm.cleaned_data['Mobile']
            address = addressForm.cleaned_data['Address']

            total = 0
            if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                if product_ids != "":
                    product_id_in_cart = product_ids.split('|')
                    products = models.Product.objects.all().filter(id__in=product_id_in_cart)
                    for p in products:
                        total += p.price

            response = render(request, 'payment.html', {'total': total})
            response.set_cookie('email', email)
            response.set_cookie('mobile', mobile)
            response.set_cookie('address', address)
            return response

        # If form is not valid, render the form again with errors
        return render(request, 'customer_address.html', {'addressForm': addressForm})
  
class payment_success_view(View):
    def get(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        products = None
        email = None
        mobile = None
        address = None

        if 'product_ids' in request.COOKIES:
            product_ids = request.COOKIES['product_ids']
            if product_ids != "":
                product_id_in_cart = product_ids.split('|')
                products = Product.objects.filter(id__in=product_id_in_cart)

        if 'email' in request.COOKIES:
            email = request.COOKIES['email']
        if 'mobile' in request.COOKIES:
            mobile = request.COOKIES['mobile']
        if 'address' in request.COOKIES:
            address = request.COOKIES['address']

        for product in products:
            Orders.objects.get_or_create(
                customer=customer,
                product=product,
                status='Pending',
                email=email,
                mobile=mobile,
                address=address
            )

        response = render(request, 'payment_success.html')
        response.delete_cookie('product_ids')
        response.delete_cookie('email')
        response.delete_cookie('mobile')
        response.delete_cookie('address')
        return response




class my_order_view(View):

    def get(self):
        customer = Customer.objects.get(user_id=self.request.user.id)
        orders = Orders.objects.filter(customer_id=customer)
        ordered_products = []

        for order in orders:
            product = Product.objects.get(id=order.product.id)
            ordered_products.append(product)

        return zip(ordered_products, orders)

    def post(self):
        pass
 


# admin view customer table
@login_required(login_url='adminlogin')
def view_customer_view(request):
    customers=models.Customer.objects.all()
    return render(request,'view_customer.html',{'customers':customers})

# admin delete customer
@login_required(login_url='adminlogin')
def delete_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view-customer')


@login_required(login_url='adminlogin')
def update_customer_view(request,pk):
    customer=models.Customer.objects.get(id=pk)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('view-customer')
    return render(request,'admin_update_customer.html',context=mydict)

# admin view the product
@login_required(login_url='adminlogin')
def admin_products_view(request):
    products=models.Product.objects.all()
    return render(request,'admin_products.html',{'products':products})


# admin add product by clicking on floating button
@login_required(login_url='adminlogin')
def admin_add_product_view(request):
    productForm=forms.ProductForm()
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST, request.FILES)
        if productForm.is_valid():
            productForm.save()
        return HttpResponseRedirect('admin-products')
    return render(request,'admin_add_products.html',{'productForm':productForm})


@login_required(login_url='adminlogin')
def delete_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    product.delete()
    return redirect('admin-products')


@login_required(login_url='adminlogin')
def update_product_view(request,pk):
    product=models.Product.objects.get(id=pk)
    productForm=forms.ProductForm(instance=product)
    if request.method=='POST':
        productForm=forms.ProductForm(request.POST,request.FILES,instance=product)
        if productForm.is_valid():
            productForm.save()
            return redirect('admin-products')
    return render(request,'admin_update_product.html',{'productForm':productForm})


@login_required(login_url='adminlogin')
def admin_view_booking_view(request):
    orders=models.Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders:
        ordered_product=models.Product.objects.all().filter(id=order.product.id)
        ordered_by=models.Customer.objects.all().filter(id = order.customer.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'admin_view_booking.html',{'data':zip(ordered_products,ordered_bys,orders)})



@login_required(login_url='adminlogin')
def delete_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin-view-booking')

# for changing status of order (pending,delivered...)
@login_required(login_url='adminlogin')
def update_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    orderForm=forms.OrderForm(instance=order)
    if request.method=='POST':
        orderForm=forms.OrderForm(request.POST,instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('admin-view-booking')
    return render(request,'update_order.html',{'orderForm':orderForm})



def Logout_page(request):
    logout(request)
    return redirect('Login_page')





