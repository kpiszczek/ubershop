from django.db import models
from django.contrib import admin

from base.models import BaseItem

class GroupOffer(BaseItem):
    price = models.DecimalField(max_digits=15,decimal_places=2)
    min_num_buyers = models.IntegerField()
    availiability_status = models.ForeignKey('core.AvailiabilityStatus')
    current_stock = models.IntegerField()
    buyers = models.ManyToManyField('core.ShopUser')
    current_num_buyers = models.IntegerField()
    
class GroupOfferAdmin(admin.ModelAdmin):
    pass

admin.site.register(GroupOffer,GroupOfferAdmin)