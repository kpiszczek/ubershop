from django.db import models
from django.contrib import admin

class Board(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    staff_only = models.BooleanField()
    
    def __unicode__(self):
        return str(self.name)
    
class Topic(models.Model):
    title = models.CharField(max_length=100)
    board = models.ForeignKey('Board')
    created_by = models.ForeignKey('core.ShopUser',blank=True,null=True)
    messages = models.ManyToManyField('Message',related_name='messages',blank=True,null=True)
    date = models.DateTimeField()
    is_active = models.BooleanField()
    
    def __unicode__(self):
        return str(self.title)
    
class Message(models.Model):
    topic = models.ForeignKey('Topic',related_name='topic')
    submitted_by = models.ForeignKey('core.ShopUser',blank=True,null=True)
    submission_date = models.DateTimeField()
    content = models.TextField()
    score = models.IntegerField(null=True,blank=True)
    prev_message = models.ForeignKey('Message',related_name='prev',blank=True,null=True)
    next_message = models.ForeignKey('Message',related_name='next',blank=True,null=True)
    
    def __unicode__(self):
        return str(self.topic)
    
class BoardAdmin(admin.ModelAdmin):
    pass

class TopicAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Board,BoardAdmin)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Message,MessageAdmin)