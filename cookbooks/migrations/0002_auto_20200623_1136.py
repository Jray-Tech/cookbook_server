# Generated by Django 2.2.8 on 2020-06-23 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbooks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='type',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='vegetarian',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='IngredientType',
        ),
    ]