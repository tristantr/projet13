from django import forms
from accounts.models import Comment

class CommentForm(forms.Form):
    place = forms.IntegerField(widget=forms.HiddenInput())
    body = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(
            attrs={
            "id":"pseudo",
            "class": "form-control",
            "placeholder": "Ajouter un commentaire",
            "style": "font-size: 1.1rem",
            }))