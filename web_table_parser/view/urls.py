from django.urls import path
from view import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'learning_logs'
urlpatterns = [
    # Домашняя страница.
    path('', views.index, name='index'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
