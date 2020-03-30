from django import forms
from .models import Comment

class comment_form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body': 'Tell us your opinion:'}