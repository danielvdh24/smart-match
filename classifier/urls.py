from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="Home"),
    path('results/', views.classify_resume, name='classify_resume'), path("execute-command/", views.execute_command, name="execute_command"),
    path('upload_csv/', views.upload_csv, name='upload_csv')
]