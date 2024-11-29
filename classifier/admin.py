from django.contrib import admin
from . import models
from django.contrib.admin.apps import AdminConfig

# Create a custom AdminConfig class to specify a custom admin site
class ClassifierAdminConfig(AdminConfig):
    default_site = "blog.admin.ClassifierAdminArea"

# Create a custom AdminSite
class ClassifierAdminArea(admin.AdminSite):
    site_header = "Classifier admin area"

# Create an instance of the custom AdminSite
classifier_site = ClassifierAdminArea(name="ClassifierAdmin")

# Register the model with the custom admin site
classifier_site.register(models.Resume)

# If you want to add more models to the custom admin site, you can do so here
# classifier_site.register(models.YourModel)
