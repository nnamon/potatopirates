from django.contrib import admin
from velocity.models import Store, Product, CustomerProfile, Receipt, Purchase

# Register your models here.


admin.site.register(Store)
admin.site.register(Product)
admin.site.register(CustomerProfile)
admin.site.register(Receipt)
admin.site.register(Purchase)
