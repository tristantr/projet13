from django import forms
from accounts.models import Comment

class CommentForm(forms.Form):
    # body = forms.Textarea(attrs={'class': 'form-control'})
    body = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
            "id":"pseudo",
            "class": "form-control",
            "placeholder": "Ajouter un commentaire",
            "style": "font-size: 1.1rem",
            }))