from django.shortcuts import render, HttpResponseRedirect, reverse
from djangodemo.models import RecipeItem, Author
from djangodemo.forms import AddRecipe, AddAuthor, LoginForm, SignupForm, RecipeUpdate
from djangodemo.settings import BASE_DIR


# auth Package imports
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def recipe_detail_view(request, pk):
    result = RecipeItem.objects.filter(id=pk)
    return render(request, 'recipe_view.html', {'data': result})


def recipes_view(request):
    print(BASE_DIR)
    results = RecipeItem.objects.all()
    return render(request, 'recipes_view.html', {'data': results})


def success_view(request):
    print(request)
    
    string = ''
    if request.method == 'POST':
        print(request)
        for x in request:
            string+=str(x)
    print(string)

    return render(request, 'thanks.html')


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


def update_recipe_view(request, pk):
    html = 'recipeitem_update_form.html'
    form = None

    if request.method == 'GET':
        form = RecipeUpdate()

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
