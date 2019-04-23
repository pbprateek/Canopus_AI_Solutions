import logging
import os
import base64
from django.http import JsonResponse

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render

from DLPart.colorize import colorme
from DLPart.face_recog import verify_if_same


def colorizeAPI(request):  # colorization logic
    logger = logging.getLogger(__name__)
    img = request.FILES['image']
    path = default_storage.save('tmp/deep.jpeg', ContentFile(img.read()))
    logger.error(path)
    tmp_file = os.path.join(settings.STATIC_ROOT, path)
    colorme('canopus/media/'+path, path)
    path = "http://127.0.0.1:8000/static/image/images/" + path
    img = {'image': path}
    # return render(request, 'image/colorize.html', img)
    return JsonResponse(img)


def faceRecogApi(request):
    logger = logging.getLogger(__name__)
    img = request.FILES['image1']
    path1 = default_storage.save('tmp/style1.jpeg', ContentFile(img.read()))
    img = request.FILES['image2']
    path2 = default_storage.save('tmp/style2.jpeg', ContentFile(img.read()))
    same_person = verify_if_same('canopus/media/'+path1, 'canopus/media/'+path2)
    dic1 = {'same_person': same_person}
    # return render(request, 'image/facerecog.html', dic1)
    return JsonResponse(dic1)
