from django import template
from post.models import Magazine, Post
from django.shortcuts import render


register = template.Library()


# @register.simple_tag()
# def get_posts_in_magazine(request, name):
#     """Вывод всех постов магазина"""
#     link = Post.objects.filter(magazine__market__username=name)
#     return render(request, 'post/magazine_posts.html', locals())


@register.inclusion_tag('post/tags/last_magazine.html')
def get_last_magazines(count=5):
    magazine = Magazine.objects.order_by("id")[:count]
    return {"last_magazines": magazine}

