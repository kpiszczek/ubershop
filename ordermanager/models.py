from django.db import models

class ShipmentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=15,decimal_places=2)
    
class OrderStatus(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
class OrderItem(models.Model):
    item = models.ForeignKey('base.BaseItem')
    order = models.ForeignKey('Order',blank=True,null=True,related_name='order')
    quantity = models.IntegerField()
    
class Order(models.Model):
    items = models.ForeignKey('OrderItem',related_name='items')
    placed_by = models.ForeignKey('core.ShopUser')
    status = models.ForeignKey('OrderStatus')
    shipment_method = models.ForeignKey('ShipmentMethod')
    date = models.DateTimeField()
    details = models.TextField()
    payment_date = models.DateTimeField(blank=True,null=True)
    