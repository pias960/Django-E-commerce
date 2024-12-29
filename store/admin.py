from django.contrib import admin
from .models import *
from import_export.admin  import  ImportExportModelAdmin

# Register your models here.
class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    prepopulated_fields = {'slug': ('name', )}
    
admin.site.register(Carts)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Banner)
admin.site.register(BillingDetails)
admin.site.register(Orders,ImportExportModelAdmin)