from django.urls import path

from . import views


urlpatterns = [
    path("post/", views.PostView.as_view()),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path("", views.home, name='home'),
    path("review/<int:pk>/", views.AddReview.as_view(), name='add_review'),
    path("about/<str:slug>", views.MagazineView.as_view(), name='magazine_detail'),
    path('market/<str:username>', views.MagazinePostListView.as_view(), name='magazine_posts'),
    path("add-rating", views.AddStarRating.as_view(), name='add_rating'),
    path("<slug:slug>/", views.PostDetailView.as_view(), name='post_detail'),

]