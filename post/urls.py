from django.urls import path

from . import views


urlpatterns = [
    path("", views.PostView.as_view()),
    path("<slug:slug>/", views.PostDetailView.as_view(), name='post_detail')
]