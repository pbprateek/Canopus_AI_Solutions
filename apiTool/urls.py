from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'get-colored-image/', views.colorizeAPI, name='colorizeAPI'),
    url(r'recognize-face/', views.faceRecogApi, name='faceRecogAPI'),
]

