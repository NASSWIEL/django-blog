from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    custom_category = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter custom category',
            'style': 'display: none;'  # Hidden by default
        }),
        help_text="This field appears when 'Something else' is selected"
    )
    
    class Meta:
        model = Post
        fields = ['title', 'category', 'custom_category', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'onchange': 'toggleCustomCategory(this.value)'
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
    
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        custom_category = cleaned_data.get('custom_category')
        
        # If "Something else" is selected, require a custom category
        if category == 'other' and not custom_category:
            raise forms.ValidationError("Please enter a custom category when 'Something else' is selected.")
        
        # If not "Something else", clear custom category
        if category != 'other':
            cleaned_data['custom_category'] = ''
            
        return cleaned_data