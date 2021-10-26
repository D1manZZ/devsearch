from django.urls import path
from .views import *

urlpatterns = [
    path('', projects, name='projects'),
    path('project/<int:pk>/', project, name='project'),
    path('add_project/', add_project, name='add_project'),
    path('edit_project/<int:pk>/', edit_project, name='edit_project'),
    path('delete_project/<int:pk>/', delete_project, name='delete_project')
]