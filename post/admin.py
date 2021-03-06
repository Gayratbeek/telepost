from django.contrib import admin
from django.contrib.gis import forms
from django.utils.safestring import mark_safe
from .models import Category, Magazine, Post, PostImages, Rating, RatingStar, Reviews


from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Post
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)
    fields = ("name",)




class ReviewInlines(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class ImageInlines(admin.TabularInline):
    model = PostImages
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "magazine", "draft")
    list_filter = ("category",)
    search_fields = ("title", "category__name",)
    inlines = [ImageInlines, ReviewInlines]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    form = PostAdminForm
    fieldsets = (
        (None, {
            "fields": ("title",)
        }),
        (None, {
            "fields": ("description", ("price", "old", "poster", "get_image"),)
        }),
        (None, {
            "fields": ("magazine", "category", "draft",)
        }),
        (None, {
            "fields": ('characteristics',)
        }),
    )
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "post", "id")



@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ("market", "delivery", "click_uz",)
    fields = ("market", "telelink", "delivery", "click_uz",)
    list_editable = ("delivery", "click_uz",)


@admin.register(PostImages)
class PostImagesAdmin(admin.ModelAdmin):
    list_display = ("titleimage", "post", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "post", "ip")

admin.site.register(RatingStar)


def get_image(url):
    return mark_safe(f'<img src={url} width="100" height="40"')

admin.site.site_title = "Админка постов"
admin.site.site_header = mark_safe(f'<img src="/media/logo.png" width="100" height="40">Администрация сайта')
