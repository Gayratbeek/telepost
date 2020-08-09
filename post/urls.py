from django.urls import path

from . import views


urlpatterns = [
    path("", views.PostView.as_view()),
    path("home/", views.home),
    path("category/<str:url>", views.move_category, name='move_category'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<str:slug>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<str:slug>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path("review/<int:pk>/", views.AddReview.as_view(), name='add_review'),
    path("about/<str:slug>", views.MagazineView.as_view(), name='magazine_detail'),
    path('market/<str:username>', views.MagazinePostListView.as_view(), name='magazine_posts'),
    path("add-rating", views.AddStarRating.as_view(), name='add_rating'),
    path("product/<slug:slug>/", views.PostDetailView.as_view(), name='post_detail'),

]