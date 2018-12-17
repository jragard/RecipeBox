from django import forms


class AddRecipe(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(AddRecipe, self).__init__(*args, **kwargs)
        self.fields['author'].choices = [(user.id, user.username)]

    title = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    author = forms.ChoiceField()
    time_required = forms.CharField(max_length=50)
    instructions = forms.CharField(widget=forms.Textarea)


class AddAuthor(forms.Form):
    name = forms.CharField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea)


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
