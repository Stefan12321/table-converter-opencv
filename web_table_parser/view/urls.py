from django.urls import path
from view import views

app_name = 'learning_logs'
urlpatterns = [
    # Домашняя страница.
    path('', views.index, name='index'),
]
