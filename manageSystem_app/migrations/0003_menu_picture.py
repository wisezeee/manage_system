# Generated by Django 4.2.2 on 2023-06-07 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manageSystem_app', '0002_alter_orderdish_options_remove_menu_dishes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='menu_pictures/', verbose_name='picture'),
        ),
    ]
