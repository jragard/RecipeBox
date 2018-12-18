# Generated by Django 2.1.3 on 2018-12-17 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangodemo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipeitem',
            name='favorited',
        ),
        migrations.AddField(
            model_name='recipeitem',
            name='favorited',
            field=models.ManyToManyField(related_name='_recipeitem_favorited_+', to='djangodemo.RecipeItem'),
        ),
    ]