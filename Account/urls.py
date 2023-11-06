
from django.contrib import admin
from django.urls import path
from Account import views
from django.contrib.auth.views import LoginView,LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('',views.home_view,name=''),

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # Customer Auth
    path('customersignup', views.customer_signup_view.as_view(),name="customersignup"),
    path("customerlogin/",views.customer_login.as_view(),name="customerlogin"),
    path('logout', LogoutView.as_view(template_name='logout.html'),name='logout'),

    #________________________________________________________________________________________________
    
    # Customer Home
    path('customer-home', views.customer_home_view,name='customer-home'),

    #________________________________________________________________________________________________

    # Customer Activities urls
    path('my-order', views.my_order_view.as_view(),name='my-order'),
    path('cart', views.cart_view.as_view(),name='cart'),
    path('add-to-cart/<int:pk>', views.add_to_cart_view.as_view(),name='add-to-cart'),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view.as_view(),name='remove-from-cart'),
    path('customer-address', views.customer_address_view.as_view(),name='customer-address'),
    path('payment-success', views.payment_success_view.as_view(),name='payment-success'),

    #_______________________________________________________________________________________________

    # Customer Profile
    path('my-profile', views.my_profile_view,name='my-profile'),
    path('edit-profile', views.edit_profile_view.as_view(),name='edit-profile'),

    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    # Admin Auth
    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='adminlogin.html'),name='adminlogin'),
    path('accounts/profile/', views.admin_dashboard_view, name='profile-view'),
    #____________________________________________________________________________________________________


    # Admin Activities ulrs
    path('view-customer', views.view_customer_view,name='view-customer'),
    path('delete-customer/<int:pk>', views.delete_customer_view,name='delete-customer'),
    path('update-customer/<int:pk>', views.update_customer_view,name='update-customer'),
    path('admin-products', views.admin_products_view,name='admin-products'),
    path('admin-add-product', views.admin_add_product_view,name='admin-add-product'),
    path('delete-product/<int:pk>', views.delete_product_view,name='delete-product'),
    path('update-product/<int:pk>', views.update_product_view,name='update-product'),

    path('admin-view-booking', views.admin_view_booking_view,name='admin-view-booking'),
    path('delete-order/<int:pk>', views.delete_order_view,name='delete-order'),
    path('update-order/<int:pk>', views.update_order_view,name='update-order'),

    #__________________________________________________________________________________________
 
   
]


    

