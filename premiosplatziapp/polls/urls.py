from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    # Question Index View (URL example: /polls/)
    path("", views.IndexView.as_view(), name="index"),
    # Question Detail View (URL example: /polls/5/)
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # Question Results View (URL example: /polls/5/results/)
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # Question Vote View (URL example: /polls/5/vote/)
    path("<int:question_id>/vote/", views.vote, name="vote"),
]