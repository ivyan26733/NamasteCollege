from django import forms
from .models import DComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = DComment
        fields = ['content']


from django import forms
from .models import DPost

class PostForm(forms.ModelForm):
    class Meta:
        model = DPost
        fields = ['title', 'image', 'content']
