from django.db import models
from base.models import BaseItem
from django.contrib import admin

class EShopItem(models.Model):
    price = models.DecimalField(max_digits=15,decimal_places=2)
    is_on_sale = models.BooleanField(default=False)
    discount_price = models.DecimalField(max_digits=15,decimal_places=2)
    availiability_status = models.ForeignKey('core.AvailiabilityStatus')
    current_stock = models.IntegerField()
    base = models.OneToOneField(BaseItem)
    
    def __str__(self):
        return str(self.base.name)

class ProductWatcher(models.Model):
    user = models.ForeignKey('core.ShopUser')
    product = models.ForeignKey('EShopItem')

class ShoppingCart(models.Model):
    user = models.ForeignKey('core.ShopUser')
    items = models.ManyToManyField('ordermanager.OrderItem')
    
class EShopItemAdmin(admin.ModelAdmin):
    pass

class ProductWatcherAdmin(admin.ModelAdmin):
    pass

class ShoppingCartAdmin(admin.ModelAdmin):
    pass

admin.site.register(EShopItem,EShopItemAdmin)
admin.site.register(ProductWatcher,ProductWatcherAdmin)
admin.site.register(ShoppingCart,ShoppingCartAdmin)