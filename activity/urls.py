from django.urls import path
import activity.views as views

urlpatterns = [
    path('addreview/<slug:game_slug>', views.add_review, name='addReview'),
    path('like-review/<int:review_id>/', views.like_review, name='like_review'),
]