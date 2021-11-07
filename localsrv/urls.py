
from django.urls import path
from .views import project_search


urlpatterns = [
    path("<str:project>/search/", project_search)
]
