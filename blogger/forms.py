from .models import *
from django import forms
from .models import Comment



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','img','Category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full bg-gray-50 dark:bg-gray-700 rounded-lg p-3 text-gray-700 dark:text-white',
                'placeholder': 'Write your comment...',
                'rows': 3,
            }),
        }
        labels = {
            'content': '',
        }

