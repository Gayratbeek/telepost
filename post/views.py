from django.shortcuts import render
from django.views.generic.base import View

from .models import Post


class PostView(View):
    """Список постов"""
    def get(self, request):
        posts = Post.objects.all()
        return render(request, "posts/post_list.html", {"post_list": posts})