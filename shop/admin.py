from django.contrib import admin
from .models import Category, Product

class AdminCategory(admin.ModelAdmin):
    list_display = ('name', 'date_added')

class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'created_at', 'stock', 'badge']

admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategory)
