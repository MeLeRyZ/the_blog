from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title  = models.CharField(max_length=200)
    text   = models.TextField()
    created_date   = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.created_date = timezone.now()
        self.save()
    
    def snippet(self):
        return self.text[:100] + '...'
    
    def list_comments(self):
        return self.comments.all()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_date']

    def publish(self):
        self.save()

    def __str__(self):
        return self.text
    
    # def children(self):
    #     return Comment.objects.filter(parent=self)
    
    # @property
    # def is_parent(self):
    #     if self.parent is not None:
    #         return False 
    #     return True