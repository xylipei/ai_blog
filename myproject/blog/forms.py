from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '您的名字'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '您的邮箱'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '在此输入您的评论', 'rows': 5}),
        }
        labels = {
            'name': '姓名',
            'email': '电子邮箱',
            'body': '评论内容'
        } 