from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
     name = models.CharField(max_length= 50)
     slug = models.SlugField()
     category = models.ForeignKey(Category,on_delete=models.CASCADE)
     price = models.DecimalField(max_digits=10, decimal_places=2)
     image = models.ImageField(upload_to ="photos/",null=True,blank=True)
     description = models.TextField()
     stock = models.PositiveIntegerField(default = 0)
     is_available = models.BooleanField(default = True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     def __str__(self):
       return self.name

class Order(models.Model):
     STATUS_CHOICES = [
         ("pending", "pending"),
         ("confirmed","confirmed"),
         ("shipping","shipping"),
         ("delivered","delivered"),
         ("cancelled","cancelled"),
     ]
     PAYMENT_CHOICES =[
         ('COD','Cash on Delivery'),
         ('Card','card(demo)'),
     ]
     user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="orders")
     total_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
     status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending")
     created_at = models.DateTimeField(auto_now_add=True)
     full_name = models.CharField(max_length=50,default="")
     phone = models.CharField(max_length=20,default="")
     city = models.CharField(max_length=50,default="")
     address = models.TextField(default="")
     payment = models.CharField(max_length=20,choices=PAYMENT_CHOICES,default="COD")

     def __str__(self):
         return f'Order {self.user}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
   
    def __str__(self):
        return f"Order {self.order} - {self.product.name} - {self.price}"

    @property
    def subtotal(self):
        return self.price * self.quantity
    