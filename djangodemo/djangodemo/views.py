from django.shortcuts import render, HttpResponseRedirect, reverse
# from django.http import HttpResponse
from djangodemo.models import RecipeItem, Author
from djangodemo.forms import AddRecipe, AddAuthor, LoginForm, SignupForm

# auth Package imports
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# def news_view(request):

#     results = NewsItem.objects.filter(author__id=2)

#     return render(request, 'news_view.html', {'data': results})


def recipe_detail_view(request, pk):

    result = RecipeItem.objects.filter(id=pk)

    return render(request, 'recipe_view.html', {'data': result})


def recipes_view(request):

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

    if request.method == 'POST':

        form = AddRecipe(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data

            RecipeItem.objects.create(
                title=data['title'],
                body=data['body'],
                author=Author.objects.filter(id=data['author']).first()
            )
            return HttpResponseRedirect(reverse('homepage'))
    else:
        # everything we get here is going to a GET request
        form = AddRecipe(user=request.user)

    return render(request, html, {'form': form})


def add_author_view(request):
    html = 'add_author.html'
    form = None

    if request.method == 'POST':

        form = AddAuthor(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            Author.objects.create(
                name=data['name'],
                life_story=data['life_story'],
            )
    #         name = models.CharField(max_length=50)
    # life_story = models.TextField(max_length=4000)
            return HttpResponseRedirect(reverse('homepage'))
    else:
        # everything we get here is going to a GET request
        form = AddAuthor()

    return render(request, html, {'form': form})


@login_required()
def signup_view(request):
    html = 'signup.html'

    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('homepage'))
    # absantiate from post or render as a get request.
    form = SignupForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['username'], data['email'], data['password']
        )
        Author.objects.create(
                name=data['username'],
                bio=data['bio'],
                user=user
            )
        # Login is what places the session cookie on your comp
        # and sets the session in django and grants authentification
        # to login required pages.
        login(request, user)
        # Tells django to lookup the name of the view with the Name 'homepage'
        # Reverse goes backwards to figure out what the name 'homepage' refers
        # to and grabs the homepage route
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
