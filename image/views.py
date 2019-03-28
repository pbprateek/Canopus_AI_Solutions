from django.shortcuts import render
from google_images_download import google_images_download
import shutil
import os
import os.path as P
import urllib.request as urllib2
from bs4 import BeautifulSoup
import logging
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.http import JsonResponse
from DLPart.colorize import colorme


dic = dict()


def home(request):
    data = {
        'name': 'Vitor'
    }
    return render(request, 'image/base.html')
    #return JsonResponse(data)


def services(request):
    return render(request, 'image/service.html')


def imgClass(request):
    return render(request, 'image/imgclass.html')


def deepDreams(request):
    return render(request, 'image/deepdreams.html')


def styleTransfer(request):
    return render(request, 'image/styletrans.html')


def imageUpload(request):
    logger = logging.getLogger(__name__)
    img = request.FILES['image']
    path = default_storage.save('tmp/deep.jpeg', ContentFile(img.read()))
    logger.error(path)
    tmp_file = os.path.join(settings.STATIC_ROOT, path)
    colorme('canopus/media/tmp/deep.jpeg', 'abc')
    img = {'image': '000.jpg'}
    return render(request, 'image/base.html', img)


def styleUpload(request):
    logger = logging.getLogger(__name__)
    img = request.FILES['image1']
    path = default_storage.save('tmp/style1.jpeg', ContentFile(img.read()))
    img = request.FILES['image2']
    path = default_storage.save('tmp/style2.jpeg', ContentFile(img.read()))
    logger.error(path)
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    return render(request, 'image/home.html')



def downloadImages(keywords):
    response = google_images_download.googleimagesdownload()  # class instantiation

    arguments = {"keywords": keywords, "limit": 5, "print_urls": True,
                 "output_directory": "Images"}  # creating list of arguments
    paths = response.download(arguments)  # passing the arguments to the function
    print(paths)  # printing absolute paths of the downloaded images


def calculateWeights(request):
    cat1 = request.POST["input1"]
    cat2 = request.POST["input2"]
    keywords = cat1 + "," + cat2
    downloadImages(keywords)
    """ 
        Classification code goes here
    """
    dic["images"] = True
    deleteImages(cat1, cat2)
    return render(request, 'image/home.html', dic)


def deleteImages(cat1, cat2):
    try:
        print(os.getcwd())
        # path = os.getcwd()
        directory = "Pictures/" + cat1
        shutil.rmtree(directory)
        directory = "Pictures/" + cat2
        shutil.rmtree(directory)

    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    del dic["images"]
    # return render(request, 'image/home.html', dic)
