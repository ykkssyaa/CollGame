from django.urls import path
import activity.views as views

urlpatterns = [
    path('addreview/<slug:game_slug>', views.add_review, name='addReview'),
    path('like-review/<int:review_id>/', views.like_review, name='like_review'),
    path('addgamedictionary', views.add_game_dictionary, name='add_game_dictionary'),
    path('dictionary/<int:id>', views.ActivityListView.as_view(), name='dictionary_page'),
    path('dictionary/<int:pk>/update', views.UpdateDictionaryView.as_view(), name='update_dictionary'),
    path('delete', views.DeleteActivityView.as_view(), name='delete_activity'),
]