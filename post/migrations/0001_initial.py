# Generated by Django 3.0.8 on 2020-07-25 21:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Категория')),
                ('description', models.TextField(verbose_name='Описание')),
                ('url', models.SlugField(blank=True, max_length=70, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Magazine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telelink', models.CharField(max_length=100, verbose_name='Ссылка на телеграм')),
                ('delivery', models.BooleanField(default=False, verbose_name='Доставка')),
                ('click_uz', models.BooleanField(default=False, verbose_name='Онлайн платёж')),
                ('market', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Название')),
                ('poster', models.ImageField(upload_to='product_images/', verbose_name='Главное фото')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.PositiveIntegerField(default=0, help_text='Указывать в сумах', verbose_name='Стоимость')),
                ('url', models.SlugField(max_length=70, unique=True)),
                ('draft', models.BooleanField(default=False, verbose_name='Черновик')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='post.Category', verbose_name='Категория')),
                ('magazine', models.ForeignKey(default='Magazine', on_delete=django.db.models.deletion.SET_DEFAULT, to='post.Magazine', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
            },
        ),
        migrations.CreateModel(
            name='RatingStar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.SmallIntegerField(default=0, verbose_name='Значение')),
            ],
            options={
                'verbose_name': 'Звезда рейтинга',
                'verbose_name_plural': 'Звезды рейтинга',
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('text', models.TextField(max_length=5000, verbose_name='Сообщение')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='post.Reviews', verbose_name='Родитель')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Post', verbose_name='пост')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, verbose_name='IP адрес')),
                ('post', models.ForeignKey(on_delete=django.db.models.fields.CharField, to='post.Post', verbose_name='пост')),
                ('star', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.RatingStar', verbose_name='звезда')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
            },
        ),
        migrations.CreateModel(
            name='PostImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('image', models.ImageField(upload_to='product_images/', verbose_name='Изображение')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.Post', verbose_name='Пост')),
            ],
            options={
                'verbose_name': 'Фотки поста',
                'verbose_name_plural': 'Фотки поста',
            },
        ),
    ]
