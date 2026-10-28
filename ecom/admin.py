from django.contrib import admin
from .models import Category,Product,Order,OrderItem
# Register your models here.

@admin.action(description="mark product unavailable")
def mark_unavailable(modeladmin,request,queryset):
    queryset.update(is_available= False)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','price','stock','created_at','is_available')
    action = [mark_unavailable]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','status','created_at')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product','quantity','price')

