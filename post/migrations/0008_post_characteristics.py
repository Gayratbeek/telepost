# Generated by Django 3.0.8 on 2020-07-28 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_auto_20200728_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='characteristics',
            field=models.TextField(blank=True, default='Нет характеристики.', null=True, verbose_name='Характеристики'),
        ),
    ]
