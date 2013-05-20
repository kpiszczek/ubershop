from django.db import models
from jsonfield import JSONField
from django.contrib import admin

def get_path(instance,filename):
    return "files/%s/images/%s" % (instance.__class__.__name__, filename)

class BaseItem(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('core.Category')
    properties = JSONField(blank=True,null=True)
    description = models.TextField()
    thumb = models.ImageField(upload_to=get_path)
    images = models.ManyToManyField('core.Image',blank=True,null=True)
    is_active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.name)
    
class BaseItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(BaseItem,BaseItemAdmin)