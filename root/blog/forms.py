from django import forms
from .models import Comment


class EmailPostForm(forms.Form):  # form for sharing post (inherits from Form)
    name = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'youremail@gmail.com'}))
    email_to = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'recipientemail@gmail.com'}))
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):  # to dynamically build form from Model (inherits from ModelForm)
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
