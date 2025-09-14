from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # user has multiple article not the inverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now) #when the object is createsd we will assigne the current time to it 
    author = models.ForeignKey(User, on_delete=models.CASCADE) # if user is deleted their posts will be delted as well 

    def __str__(self):
        return self.title
