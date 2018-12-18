"""djangodemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from djangodemo.models import Author, RecipeItem
from djangodemo.views import (recipes_view, recipe_detail_view, 
                              author_detail_view, add_recipe_view, 
                              add_author_view, login_view, signup_view, 
                              logout_view, favorites_view, RecipeUpdate)


admin.site.register(Author)
admin.site.register(RecipeItem)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', recipes_view, name='homepage'),
    path('favorites/<str:name>', favorites_view),
    path('recipe/<int:pk>', recipe_detail_view),
    path('recipe/edit/<int:pk>', RecipeUpdate.as_view()),
    path('author/<str:name>', author_detail_view),
    path('addrecipe/', add_recipe_view),
    path('addauthor/', add_author_view, name='addauthor'),
    path('signup/', signup_view),
    path('login/', login_view),
    path('logout/', logout_view)
]
