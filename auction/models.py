from django.db import models
from django.contrib import admin

from base.models import BaseItem

class Bid(models.Model):
    user = models.ForeignKey('core.ShopUser')
    item = models.ForeignKey('AuctionItem')
    date = models.DateTimeField()
    price = models.DecimalField(max_digits=15,decimal_places=2)
    
    def __str__(self):
        return str(self.date)
    
class AuctionItem(models.Model):
    created_by = models.ForeignKey('core.ShopUser')
    start_date = models.DateTimeField()
    close_date = models.DateTimeField(blank=True,null=True)
    planned_close_date = models.DateTimeField()
    current_price = models.DecimalField(max_digits=15,decimal_places=2)
    reserve_price = models.DecimalField(max_digits=15,decimal_places=2,
                                        blank=True,null=True)
    bids = models.ManyToManyField('Bid',blank=True,null=True)
    payment_date = models.DateTimeField(blank=True,null=True)
    base = models.OneToOneField(BaseItem)
    
    def __str__(self):
        return str(self.base.name)
    
class BidAdmin(admin.ModelAdmin):
    pass

class AuctionItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Bid,BidAdmin)
admin.site.register(AuctionItem,AuctionItemAdmin)


