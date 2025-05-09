from django import forms
from .models import Comment, Post

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'pic', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.TextInput(attrs={'placeholder': '#fun #vacation'}),
        }

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']  # Changed from 'comment' to 'text'
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Add a comment...'
            }),
        }