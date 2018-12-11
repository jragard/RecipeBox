from django import forms
from djangodemo.models import Author


class AddRecipe(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    author = forms.ChoiceField()

    def __init__(self, user, *args, **kwargs):
        super(AddRecipe, self).__init__(*args, **kwargs)
        self.fields['author'].choices = [(user.id, user.username)]


class AddAuthor(forms.Form):
    name = forms.CharField(max_length=100)
    life_story = forms.CharField(widget=forms.Textarea)

    pass


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    bio = forms.CharField(widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
