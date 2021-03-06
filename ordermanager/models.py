from django.db import models
from django.contrib import admin

class ShipmentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=15,decimal_places=2)
    
    def __str__(self):
        return str(self.name)
    
class OrderStatus(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return str(self.name)
    
class OrderItem(models.Model):
    item = models.ForeignKey('base.BaseItem')
    belongs_to = models.ForeignKey('core.ShopUser')
    order = models.ForeignKey('Order',blank=True,null=True,related_name='order')
    quantity = models.IntegerField(default=0)
    
class Order(models.Model):
    items = models.ManyToManyField('OrderItem',related_name='items', blank=True)
    placed_by = models.ForeignKey('core.ShopUser')
    status = models.ForeignKey('OrderStatus')
    shipment_method = models.ForeignKey('ShipmentMethod')
    date = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True,null=True)
    payment_date = models.DateTimeField(blank=True,null=True)
    
class OrderStatusAdmin(admin.ModelAdmin):
    pass

class OrderItemAdmin(admin.ModelAdmin):
    pass

class OrderAdmin(admin.ModelAdmin):
    pass

class ShipmentMethodAdmin(admin.ModelAdmin):
    pass

admin.site.register(OrderStatus, OrderStatusAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ShipmentMethod, ShipmentMethodAdmin)
    