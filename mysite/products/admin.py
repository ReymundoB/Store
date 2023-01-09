from django.contrib import admin

# Register your models here.
from .models import Product

#modifica la vista del admin en la seccion de add product con los campos que indicamos en fields
#list_display es para mostrar campos en la listas
class ProductAdmin(admin.ModelAdmin):
    fields = ('title','description','price','image')
    list_display = ('__str__', 'slug','created_at')

admin.site.register(Product, ProductAdmin)