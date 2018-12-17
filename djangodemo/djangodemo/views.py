from django.shortcuts import render, HttpResponseRedirect, reverse
from djangodemo.models import RecipeItem, Author
from djangodemo.forms import AddRecipe, AddAuthor, LoginForm, SignupForm
from djangodemo.settings import BASE_DIR
from django.views.generic.edit import UpdateView

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


class RecipeUpdate(UpdateView):
    model = RecipeItem
    fields = ['title', 'body', 'time_required', 'instructions']
    template_name = 'recipeitem_update_form.html'


def recipe_detail_view(request, pk):
    result = RecipeItem.objects.filter(id=pk)
    for x in result:
        author = str(x.author)
    logged_in_user = str(request.user)
    return render(request, 'recipe_view.html', {'data': result, 'user': logged_in_user, 'author': author})


def recipes_view(request):
    print(BASE_DIR)
    results = RecipeItem.objects.all()
    return render(request, 'recipes_view.html', {'data': results})


def author_detail_view(request, name):
    results = Author.objects.filter(name=name)
    recipes = RecipeItem.objects.all().filter(author__name=name)
    return render(request, 'authors_view.html', {'data': results, 'recipes': recipes})


@login_required()
def add_recipe_view(request):
    html = 'add_recipe.html'
    form = None

    for aut in Author.objects.all().values():
        if request.user.id == aut['id']:
            author = aut
            break
        else:
            author = {'name': False}

    if request.method == 'POST' and str(request.user) == author['name']:
        form = AddRecipe(request.user, request.POST)

        if form.is_valid():
            data = form.cleaned_data

            RecipeItem.objects.create(
                title=data['title'],
                body=data['body'],
                author=Author.objects.filter(id=data['author']).first(),
                time_required=data['time_required'],
                instructions=data['instructions']
            )
            return HttpResponseRedirect(reverse('homepage'))

    elif request.method == 'GET' and str(request.user) == author['name']:
        form = AddRecipe(user=request.user)

    else:
        return render(request, 'unauthorized.html')

    return render(request, html, {'form': form})


def add_author_view(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('homepage'))

    html = 'add_author.html'
    form = None

    if request.method == 'POST':
        form = AddAuthor(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            Author.objects.create(
                name=data['name'],
                bio=data['bio'],
                user=data['user']
            )

            return HttpResponseRedirect(reverse('homepage'))

    else:
        form = AddAuthor()

    return render(request, html, {'form': form})


def signup_view(request):
    html = 'signup.html'
    form = SignupForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], data['email'], data['password']
        )

        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})


def login_view(request):
    html = 'login.html'
    form = LoginForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('homepage'))

    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))
