from django.contrib import admin
from . import models
from django.contrib.admin.apps import AdminConfig

# Create a custom AdminConfig class to specify a custom admin site
class ClassifierAdminConfig(AdminConfig):
    default_site = "blog.admin.ClassifierAdminArea"

# Create a custom AdminSite
class ClassifierAdminArea(admin.AdminSite):
    site_header = "Admin Area Login"
    login_template = 'admin/login.html'

# Create an instance of the custom AdminSite
classifier_site = ClassifierAdminArea(name="ClassifierAdmin")

# Customize the PredictionLog display
class PredictionLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'resume_text', 'prediction_result')
    search_fields = ('resume_text', 'prediction_result')
    list_filter = ('timestamp',)

# Register the model with the custom admin site
classifier_site.register(models.Resume)
classifier_site.register(models.PredictionLog)

# If you want to add more models to the custom admin site, you can do so here
# classifier_site.register(models.YourModel)
