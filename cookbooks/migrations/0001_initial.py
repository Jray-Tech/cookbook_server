# Generated by Django 2.2.8 on 2020-06-23 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Difficulty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('carbohydrate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('protein', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('instructions', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('time_to_complete', models.IntegerField()),
                ('recipe_image', models.ImageField(upload_to='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('difficulty', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cookbooks.Difficulty')),
                ('ingredients', models.ManyToManyField(to='cookbooks.Ingredient')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeNutrient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carbohydrate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('protein', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('recipe', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cookbooks.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='cookbooks.Tags'),
        ),
        migrations.CreateModel(
            name='IngredientUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=3)),
                ('value', models.DecimalField(decimal_places=2, max_digits=5)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookbooks.Ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cookbooks.Recipe')),
            ],
        ),
        migrations.AddField(
            model_name='ingredient',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cookbooks.IngredientType'),
        ),
        migrations.CreateModel(
            name='CategoryForTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('tags', models.ManyToManyField(to='cookbooks.Tags')),
            ],
        ),
    ]
