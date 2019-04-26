import logging
import os
import shutil
import base64
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from google_images_download import google_images_download
from DLPart.colorize import colorme
from DLPart.face_recog import verify_if_same
from django.http import JsonResponse
from DLPart.image_classification import train_weights_Image_classifier
from DLPart.style import style_transfer


dic = dict()


def home(request):
    return render(request, 'image/dashboard.html')


def services(request):
    return render(request, 'image/services.html')


def documentation(request):
    return render(request, 'image/documentation.html')


""" -----------------IMAGE CLASSIFICATION------------------------------ """


def imgClass(request):
    return render(request, 'image/imgclass.html')


def calculateWeights(request):   # Classification Logic
    cat1 = request.POST["input1"]
    cat2 = request.POST["input2"]
    accuracy = train_weights_Image_classifier(cat1, cat2)
    deleteImages(cat1, cat2)
    dic1 = {'done': True, 'Accuracy': accuracy}
    return render(request, 'image/resultImgClass.html', dic1)


""" ------------------------- COLORIZATION -------------------------"""


def colorize(request):
    return render(request, 'image/colorize.html')


def imageUpload(request):  # colorization logic
    img = request.FILES['image']
    path = default_storage.save('tmp/colored.jpeg', ContentFile(img.read()))
    colorme('canopus/media/'+path, path)
    img = {'image': path}
    return render(request, 'image/colorize.html', img)



"""--------------------------- STYLE TRANSFER -----------------------------"""


def styleTransfer(request):
    return render(request, 'image/styletransfer.html')


def styleTransferDone(request):  # Style Transfer logic
    img1 = request.FILES['image1']
    img2 = request.FILES['image2']
    img1_path = default_storage.save('tmp/style1.jpeg', ContentFile(img1.read()))
    img2_path = default_storage.save('tmp/style2.jpeg', ContentFile(img2.read()))
    style_transfer('canopus/media/'+img1_path, 'canopus/media/'+img2_path, img2_path)
    out = {'coloured_img': img2_path}
    return render(request, 'image/styletransfer.html', out)


"""-------------------------- FACIAL RECOGNITION --------------------------------"""


def faceRecognition(request):
    return render(request, 'image/facerecog.html')


def faceRecogDone(request):
    logger = logging.getLogger(__name__)
    img = request.FILES['image1']
    path1 = default_storage.save('tmp/style1.jpeg', ContentFile(img.read()))
    img = request.FILES['image2']
    path2 = default_storage.save('tmp/style2.jpeg', ContentFile(img.read()))
    same_person = verify_if_same('canopus/media/'+path1, 'canopus/media/'+path2)
    dic1 = {'same_person': same_person, 'done': True}
    return render(request, 'image/resultFaceRecog.html', dic1)



def deleteImages(cat1, cat2):
    try:
        print(os.getcwd())
        path = os.getcwd()
        print(path)
        directory = "DLPart\ImageClassifierJunk\\" + cat1 + cat2 + "\\" + cat1
        shutil.rmtree(directory)
        directory = "DLPart\ImageClassifierJunk\\" + cat1 + cat2 + "\\" + cat2
        shutil.rmtree(directory)
        directory = "DLPart\ImageClassifierJunk\\" + cat1 + cat2
        shutil.rmtree(directory)

    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    # del dic["images"]
    #return render(request, 'image/home.html', dic)
