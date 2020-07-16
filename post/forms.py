from django import forms

from .models import Reviews


class ReviewForm(forms.Form):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")