from django import forms
from django.views.generic.edit import UpdateView
from djangodemo.models import RecipeItem
from django.shortcuts import get_object_or_404


class AddRecipe(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(AddRecipe, self).__init__(*args, **kwargs)
        self.fields['author'].choices = [(user.id, user.username)]

    title = forms.CharField(max_length=100)
    body = forms.CharField(widget=forms.Textarea)
    author = forms.ChoiceField()
    time_required = forms.CharField(max_length=50)
    instructions = forms.CharField(widget=forms.Textarea)


class RecipeModelForm(forms.ModelForm):
    class Meta:
        model = RecipeItem
        fields = ['title', 'body', 'author', 'time_required', 'instructions']


class RecipeUpdate(UpdateView):
    # model = RecipeItem
    # fields = ['title', 'body', 'time_required', 'instructions']
    # template_name_suffix = '_update_form'
    template_name = 'html/recipeitem_update_form.html'
    form_class = RecipeModelForm
    # queryset = RecipeItem.objects.all()



    def get_object(self):
        # id_ = self.kwargs.get('pk')
        # print(self.kwargs['pk'])
        # print(id_)
        return RecipeItem.objects.filter(id=self.kwargs['pk']).first()

    def form_valid(self, form):
        return super().form_valid(form)
    


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
