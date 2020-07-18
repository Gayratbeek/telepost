from django.urls import path

from . import views


urlpatterns = [
    path("", views.PostView.as_view()),
    path("<slug:slug>/", views.PostDetailView.as_view(), name='post_detail'),
    path("review/<int:pk>/", views.AddReview.as_view(), name='add_review'),
    path("magazine/<str:slug>/", views.MagazineView.as_view(), name='magazine_detail'),
]