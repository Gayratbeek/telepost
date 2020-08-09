from transliterate import translit
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
from django.contrib.auth import get_user_model

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.SlugField(max_length=70, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        super(Category, self).save()
        if self.parent.mptt_level is not None:
            if self.parent.mptt_level == 3:
                raise ValueError(u'Достигнута максимальная вложенность!')
        if not self.url:
            self.url = slugify(translit(self.name, 'ru', reversed=True))
            super(Category, self).save()
        elif self.url != slugify(translit(self.name, 'ru', reversed=True)):
            self.url = slugify(translit(self.name, 'ru', reversed=True))
            super(Category, self).save()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Magazine(models.Model):
    """Магазин"""
    market = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="название")
    telelink = models.CharField("Ссылка на телеграм", max_length=100)
    delivery = models.BooleanField(default=False, verbose_name="Доставка")
    click_uz = models.BooleanField(default=False, verbose_name="Онлайн платёж")
    poster = models.ImageField("Главное фото", upload_to="product_images/", default="default.jpeg", blank=True,
                               null=True)

    def __str__(self):
        return self.market.username

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def get_absolute_url(self):
        return reverse('magazine_detail', kwargs={"slug": self.market})

    def get_magazine_posts(self):
        return reverse("magazine_posts", kwargs={"username": self.market})


class Post(models.Model):
    """Пост"""
    title = models.CharField("Название", max_length=64)
    poster = models.ImageField("Главное фото", upload_to="product_images/", default="default.jpeg", blank=True,
                               null=True)
    description = models.TextField("Описание")
    characteristics = models.TextField("Характеристики", blank=True, null=True, default="Нет характеристики.")
    price = models.PositiveIntegerField("Стоимость", default=0, help_text="Указывать в сумах")
    old = models.PositiveIntegerField("Старая цена", blank=True, null=True)
    magazine = models.ForeignKey(Magazine, verbose_name="Поставщик",
                                 on_delete=models.SET_DEFAULT, default='Magazine')
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=70, unique=True)
    draft = models.BooleanField("Черновик", default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.url})

    def get_magazine_posts(self):
        return reverse("magazine_posts", kwargs={"slug": self.magazine.market.username})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def save(self, **kwargs):
        super(Post, self).save()
        if not self.url:
            self.url = slugify(translit(self.title, 'ru', reversed=True)) + '-' + str(self.id)
            super(Post, self).save()
        elif self.url != slugify(translit(self.title, 'ru', reversed=True)):
            self.url = slugify(translit(self.title, 'ru', reversed=True))
            super(Post, self).save()


class PostImages(models.Model):
    """Изображения поста в большом количестве"""
    post = models.ForeignKey(Post, verbose_name="Пост", blank=True, null=True, on_delete=models.CASCADE, default=None)
    titleimage = models.CharField("Заголовок", max_length=100, blank=True, null=True, default="image_title")
    # description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="product_images/", blank=True, null=True, default="Изображение "
                                                                                                         "продукта")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = None

    def __str__(self):
        return self.titleimage

    class Meta:
        verbose_name = "Фотки поста"
        verbose_name_plural = "Фотки поста"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Звезда рейтинга"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="пост")

    def __str__(self):
        return f"{self.star} - {self.post}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Родитель",
                               on_delete=models.SET_NULL, blank=True, null=True)
    post = models.ForeignKey(Post, verbose_name="пост", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.post}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
