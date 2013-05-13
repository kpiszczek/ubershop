from django.db import models
from jsonfield import JSONField
from django.contrib import admin

from django.contrib.auth.models import User

def get_path(name):
    raise NotImplemented

class Permission(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Category(models.Model):
    name = models.CharField(max_length=100)
    properties = JSONField(blank=True,null=True)
    
    def __unicode__(self):
        return str(self.name)
    
class Image(models.Model):
    image = models.ImageField(upload_to=get_path)
    
class AvailiabilityStatus(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __unicode__(self):
        return str(self.name)
    
class ShipmentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
class ShopUser(models.Model):
    user = models.OneToOneField(User)
    permissions = models.ManyToManyField('Permission')
    organisation = models.TextField()
    address = models.TextField()
    tax_id = models.CharField(max_length=40)
    watched_products = models.ManyToManyField('eshop.ProductWatcher')
    discount = models.DecimalField(max_digits=4,decimal_places=2)
    total_spendings = models.DecimalField(max_digits=15,decimal_places=2)
    
class PermissionAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass

class AvailiabilityStatusAdmin(admin.ModelAdmin):
    pass

class ShipmentMethodAdmin(admin.ModelAdmin):
    pass

class ShopUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Permission,PermissionAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(AvailiabilityStatus,AvailiabilityStatusAdmin)
admin.site.register(ShopUser, ShopUserAdmin)
    