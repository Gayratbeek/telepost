# Generated by Django 3.0.8 on 2020-07-26 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20200725_2152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postimages',
            old_name='title',
            new_name='titleimage',
        ),
    ]