from django.contrib import admin

from .models import Category, Magazine, Post, PostImages, Rating, RatingStar, Reviews


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class RevieInlines(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category",)
    search_fields = ("title", "category__name",)
    inlines = [RevieInlines]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    fields = ()

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "parent", "post", "id")
    readonly_fields = ("name", "email")



admin.site.register(Magazine)
admin.site.register(PostImages)
admin.site.register(Rating)
admin.site.register(RatingStar)





