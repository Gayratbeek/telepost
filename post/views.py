from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Post, Magazine
from .forms import ReviewForm


class PostView(ListView):
    """Список постов"""
    model = Post
    queryset = Post.objects.filter(draft=False)
    #template_name = "posts/post_list.html"


class PostDetailView(DetailView):
    """Полное описание фильма"""
    model = Post
    slug_field = 'url'
    #template_name = "posts/post_detail.html"


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        posting = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.post = posting
            form.save()
        return redirect(posting.get_absolute_url())


class MagazineView(DetailView):
    model = Magazine
    template_name = 'post/magazine.html'
    slug_field = "name"