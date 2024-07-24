from django.contrib import admin
from .models import Vendor, Product

class VendorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'phone_number', 'email', 'role', 'get_products', 'created_at')
    search_fields = ('name', 'email', 'role')
    list_filter = ('role', 'created_at')

    def get_products(self, obj):
        products = Product.objects.filter(vendor=obj)
        product_list = [product.name for product in products]
        return ", ".join(product_list)

    get_products.short_description = 'Products'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'vendor', 'name', 'category', 'price', 'quantity', 'description', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('category', 'created_at')

admin.site.register(Vendor, VendorAdmin)
admin.site.register(Product, ProductAdmin)
