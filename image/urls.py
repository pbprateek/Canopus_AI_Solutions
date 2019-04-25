from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'services/', views.services, name='services'),
    url(r'documentation/', views.documentation, name='documentation'),
    url(r'img-classification/', views.imgClass, name='imgClass'),
    url(r'img-classification-done/', views.calculateWeights, name='classificationDone'),
    url(r'colorize/', views.colorize, name='colorize'),
    # url(r'colorize-done/', views.imageUpload, name='colorizationDone'),
    url(r'style-transfer/', views.styleTransfer, name='styleTransfer'),
    url(r'style-transfer-done/', views.styleTransferDone, name='styleTransferDone'),
    url(r'face-recognition/', views.faceRecognition, name='faceRecognition'),
    # url(r'face-recognition-done', views.faceRecogDone, name='faceRecognitionDone'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)