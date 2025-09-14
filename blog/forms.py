from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Write your post content here...'
            })
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        # If editing, exclude the current post from the duplicate check
        if self.instance and self.instance.pk:
            if Post.objects.filter(title=title).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("A post with this title already exists. Please choose a different title.")
        else:
            if Post.objects.filter(title=title).exists():
                raise forms.ValidationError("A post with this title already exists. Please choose a different title.")
        return title