from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'colorit/', views.colorizeAPI, name='colorizeAPI'),
    url(r'recognizeface/', views.faceRecogApi, name='faceRecogAPI'),
    url(r'simply/', views.simple, name='faceRecogAPI')
]
