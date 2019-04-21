import logging
import os
import shutil
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from google_images_download import google_images_download
from DLPart.colorize import colorme
from DLPart.face_recog import verify_if_same

dic = dict()


def home(request):
    return render(request, 'image/dashboard.html')


def services(request):
    return render(request, 'image/services.html')


def documentation(request):
    return render(request, 'image/documentation.html')


def imgClass(request):
    return render(request, 'image/imgclass.html')


def deepDreams(request):
    return render(request, 'image/deepdreams.html')


def styleTransfer(request):
    return render(request, 'image/styletransfer.html')


def faceRecognition(request):
    return render(request, 'image/facerecog.html')


def imageUpload(request):
    logger = logging.getLogger(__name__)
    img = request.FILES['image']
    path = default_storage.save('tmp/deep.jpeg', ContentFile(img.read()))
    oldpath = default_storage.save('tmp/deep.jpeg', ContentFile(img.read()))
    colorme('canopus/media/'+path, path)
    img = {'image': path, 'oldimage': 'canopus/media/'+oldpath}
    return render(request, 'image/result.html', img)


def styleUpload(request):
    logger = logging.getLogger(__name__)
    img = request.FILES['image1']
    path1 = default_storage.save('tmp/style1.jpeg', ContentFile(img.read()))
    img = request.FILES['image2']
    path2 = default_storage.save('tmp/style2.jpeg', ContentFile(img.read()))
    same_person = verify_if_same('canopus/media/'+path1,'canopus/media/'+path2)
    dict = {'same_person':same_person}
    return render(request, 'image/facerecog.html',dict)



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
