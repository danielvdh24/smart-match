from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="Home"),
    path('results/', views.classify_resume, name='classify_resume'), path("train-command/", views.train_command, name="train_command"),
    path('upload_csv/', views.upload_csv, name='upload_csv'), path("fetch-latest-model/", views.fetch_latest_model, name="fetch_latest_model"), path('fetch-all-models/', views.fetch_all_models, name='fetch_all_models'), path('evaluate-command/', views.evaluate_command, name='evaluate_command')
]