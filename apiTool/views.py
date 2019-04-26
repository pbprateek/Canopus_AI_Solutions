from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from DLPart.colorize import colorme
from DLPart.face_recog import verify_if_same


@csrf_exempt
def colorizeAPI(request):  # colorization logic
    # img = request.FILES['image']
    myfile = request.FILES['image']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    colorme('canopus' + uploaded_file_url, uploaded_file_url, api=True)
    path = "http://127.0.0.1:8000/canopus" + uploaded_file_url
    hello = {"image": path}
    return JsonResponse(hello)

@csrf_exempt
def faceRecogApi(request):
    # img = request.FILES['image']
    myfile1 = request.FILES['image1']
    myfile2 = request.FILES['image2']
    fs = FileSystemStorage()
    filename1 = fs.save(myfile1.name, myfile1)
    uploaded_file_url1 = fs.url(filename1)

    filename2 = fs.save(myfile2.name, myfile2)
    uploaded_file_url12 = fs.url(filename2)

    same = verify_if_same('canopus' + uploaded_file_url1, 'canopus' + uploaded_file_url12)

    hello = {"same_person": same}
    return JsonResponse(hello)


