from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from .models import Post, Magazine, Rating, PostImages, Category
from .forms import ReviewForm, RatingForm
from django.contrib.auth.models import User


from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import Category
from mptt.exceptions import InvalidMove
from mptt.forms import MoveNodeForm


def move_category(request, url):
    category_in = get_object_or_404(Category, url=url)

    if request.method == 'POST':
        form = MoveNodeForm(category_in, request.POST)
        if form.is_valid():
            try:
                category_in = form.save()
                return HttpResponseRedirect(category.get_absolute_url())
            except InvalidMove:
                pass
    else:
        form = MoveNodeForm(category_in)
    context = {
        'form': form,
        'category': category_in,
        'category_tree': Category.objects.filter(mptt_level=1),
    }
    return render(request, 'post/move_category.html', context)


class AllImages():
    def get_image(self):
        return PostImages.objects.all()


def get_client_ip(self, request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    return render(request, 'home.html', {})


def category(request):
    return render(request, "category.html", {'category': Category.objects.filter(level=2)})


class PostView(ListView):
    """Список постов"""
    model = Post
    queryset = Post.objects.filter(draft=False)
    paginate_by = 5


class PostDetailView(DetailView):
    """Полное описание фильма"""
    model = Post
    slug_field = 'url'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'description', 'poster']

    def form_valid(self, form):
        form.instance.magazine.market = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'description', 'characteristics', 'poster', 'price', 'old']
    slug_field = 'url'

    def form_valid(self, form):
        form.instance.magazine.market = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.magazine.market:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    slug_field = 'url'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.magazine.market:
            return True
        return False


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        posting = get_object_or_404(Post, id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.post = posting
            form.save()
        return redirect(posting.get_absolute_url())


class MagazinePostListView(ListView):
    model = Post
    template_name = 'post/magazine_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6
    # queryset = Post.objects.filter(draft=False)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(magazine__market=user)

    # order_by('-date_posted')


class MagazineView(DetailView):
    """Полное описание фильма"""
    model = Magazine
    context_object_name = 'mpost'
    slug_field = 'market__username'
    template_name = "market/market_detail.html"


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                post_id=int(request.POST.get("post")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)