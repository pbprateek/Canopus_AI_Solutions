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
    data = {
        'name': 'Vitor'
    }
    return render(request, 'image/home.html')
    #return JsonResponse(data)


def services(request):
    return render(request, 'image/service.html')


def imgClass(request):
    return render(request, 'image/imgclass.html')


def calculateWeights(request):   # Classification Logic
    cat1 = request.POST["input1"]
    cat2 = request.POST["input2"]
    keywords = cat1 + "," + cat2
    downloadImages(keywords)
    """ 
        Classification code goes here. Render the same page. Result will be displayed accordingly!
    """
    dic["images"] = True
    deleteImages(cat1, cat2)
    return render(request, 'image/imgclass.html', dic)


def colorize(request):
    return render(request, 'image/colorize.html')


def imageUpload(request):  # colorization logic
    logger = logging.getLogger(__name__)
    img = request.FILES['image']
    path = default_storage.save('tmp/deep.jpeg', ContentFile(img.read()))
    logger.error(path)
    tmp_file = os.path.join(settings.STATIC_ROOT, path)
    colorme('canopus/media/'+path, path)
    img = {'image': path}
    return render(request, 'image/colorize.html', img)


def styleTransfer(request):
    return render(request, 'image/styletrans.html')


def styleTransferDone(request):  # Style Transfer logic
    """"
        Style Transfer logic goes here. Render the same page. Will use if condition to display result accordingly!
    """
    return render(request, 'image/styletrans.html')


def faceRecog(request):
    return render(request, 'image/faceRecog.html')


def styleUpload(request):   # Face Recognition logic
    logger = logging.getLogger(__name__)
    img = request.FILES['image1']
    path1 = default_storage.save('tmp/style1.jpeg', ContentFile(img.read()))
    img = request.FILES['image2']
    path2 = default_storage.save('tmp/style2.jpeg', ContentFile(img.read()))
    same_person = verify_if_same('canopus/media/'+path1, 'canopus/media/'+path2)
    dic = {'same_person': same_person, 'done': True}
    return render(request, 'image/faceRecog.html', dic)


def downloadImages(keywords):
    response = google_images_download.googleimagesdownload()  # class instantiation

    arguments = {"keywords": keywords, "limit": 5, "print_urls": True,
                 "output_directory": "Images"}  # creating list of arguments
    paths = response.download(arguments)  # passing the arguments to the function
    print(paths)  # printing absolute paths of the downloaded images


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



