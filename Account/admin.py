

from django.contrib import admin
from .models import Customer,Product,Orders



class CustomerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Customer, CustomerAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)


admin.site.register(Orders, ProductAdmin)
