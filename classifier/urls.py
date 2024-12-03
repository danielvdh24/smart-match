from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="Home"),
    path('results/', views.classify_resume, name='classify_resume')
]