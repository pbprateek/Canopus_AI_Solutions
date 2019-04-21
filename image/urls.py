from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'image-classification-done/', views.calculateWeights, name='scrape'),
    url(r'img-class/', views.imgClass, name='img'),
    url(r'colorize/', views.colorize, name='dream'),
    url(r'colorize-done/', views.imageUpload, name='imageupload'),
    url(r'style-trans/', views.styleTransfer, name='style'),
    url(r'style-transfer-done/', views.styleTransferDone, name='styleTransferDone'),
    url(r'face-recog/', views.faceRecog, name='feceRecognition'),
    url(r'recognize-done/', views.styleUpload, name='styleupload'),
    url(r'services/', views.services, name='services'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)