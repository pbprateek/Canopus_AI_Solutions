from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'return-weights/', views.calculateWeights, name='scrape'),
    url(r'img-classification/', views.imgClass, name='imgClass'),
    url(r'deep-dreams/', views.deepDreams, name='deepDreams'),
    url(r'style-transfer/', views.styleTransfer, name='styleTransfer'),
    url(r'imageUpload/', views.imageUpload, name='imageupload'),
    url(r'styleUpload/', views.styleUpload, name='styleupload'),
    url(r'face-recognition/', views.faceRecognition, name='faceRecognition'),
    url(r'services/', views.services, name='services')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)