from django.urls import path
import views

urlpatterns = [
    path('addreview/<slug:game_slug>', views.add_review, name='addReview'),
    path('deletereview/<int:id>', views.delete_review, name='deleteReview'),
]