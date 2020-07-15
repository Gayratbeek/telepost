from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Post


class PostView(ListView):
    """Список постов"""
    model = Post
    queryset = Post.objects.filter(draft=False)


class PostDetailView(DetailView):
    """Полное описание фильма"""
    model = Post
    slug_field = 'url'
