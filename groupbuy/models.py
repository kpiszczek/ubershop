from django.db import models
from django.contrib import admin

from base.models import BaseItem

class GroupOffer(models.Model):
    price = models.DecimalField(max_digits=15,decimal_places=2)
    min_num_buyers = models.IntegerField()
    availiability_status = models.ForeignKey('core.AvailiabilityStatus')
    current_stock = models.IntegerField()
    buyers = models.ManyToManyField('core.ShopUser', blank=True,null=True)
    current_num_buyers = models.IntegerField(blank=True,null=True)
    base = models.OneToOneField(BaseItem)
    
    def __str__(self):
        return str(self.base.name)
    
class GroupOfferAdmin(admin.ModelAdmin):
    pass

admin.site.register(GroupOffer,GroupOfferAdmin)