from django.urls import path
from .views import *

urlpatterns = [
    path('', PictureUploadView.as_view())
] 
