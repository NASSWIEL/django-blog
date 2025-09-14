from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # user has multiple article not the inverse


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('politics', 'Politics'),
        ('religion', 'Religion'),
        ('history', 'History'),
        ('technology', 'Technology'),
        ('science', 'Science'),
        ('culture', 'Culture'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
        ('other', 'Something else'),
    ]
    
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    custom_category = models.CharField(max_length=50, blank=True, null=True, help_text="Enter a custom category if 'Something else' is selected")
    date_posted = models.DateTimeField(default = timezone.now) #when the object is createsd we will assigne the current time to it 
    author = models.ForeignKey(User, on_delete=models.CASCADE) # if user is deleted their posts will be delted as well 

    def __str__(self):
        return self.title
    
    def get_category_display_name(self):
        """Return the display name for the category, including custom categories"""
        if self.category == 'other' and self.custom_category:
            return self.custom_category
        return dict(self.CATEGORY_CHOICES)[self.category]
