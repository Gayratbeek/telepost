from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    """Категория поста"""
    name = models.CharField("Категория", max_length=64)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=70, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def save(self):
        super(Category, self).save()
        if not self.url:
            self.url = slugify(self.name) + '-' + str(self.id)
            super(Category, self).save()


class Link(models.Model):
    name = models.CharField("Название магазина", max_length=100)
    telelink = models.CharField("Ссылка на телеграм", max_length=50)
    instalink = models.CharField("Ссылка на инстаграм", max_length=50)
    otherlink = models.CharField("Ссылка на иную страницу", max_length=100, null=True, blank=True)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"


class Magazine(models.Model):
    """Магазин"""
    market = models.OneToOneField(Link, verbose_name="Название производителя", on_delete=models.CASCADE)
    delivery = models.BooleanField(default=False, verbose_name="Доставка")
    payment_click_uz = models.BooleanField(default=False, verbose_name="Оплата онлайн")

    def __str__(self):
        return self.market.name

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def get_absolute_url(self):
        return reverse('magazine_detail', kwargs={"slug": self.market.name})

    # def save(self):
    #     super(Magazine, self).save()
    #     if not self.url:
    #         self.url = self.market.username
    #         super(Magazine, self).save()


class Post(models.Model):
    """Пост"""
    title = models.CharField("Название", max_length=64)
    poster = models.ImageField("Главное фото", upload_to="product_images/")
    description = models.TextField("Описание")
    price = models.PositiveIntegerField("Стоимость", default=0, help_text="Указывать в сумах")
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

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def save(self):
        super(Post, self).save()
        if not self.url:
            self.url = slugify(self.title) + '-' + str(self.id)
            super(Post, self).save()


class PostImages(models.Model):
    """Изображения поста в большом количестве"""
    title = models.CharField("Заголовок", max_length=100)
    # description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="product_images/")
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фотки поста"
        verbose_name_plural = "Фотки поста"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"


class Rating(models.Model):
    """Звезда рейтинга"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    post = models.ForeignKey(Post, on_delete=models.CharField, verbose_name="пост")

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

    def __str__(self):
        return f"{self.name} - {self.post}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"