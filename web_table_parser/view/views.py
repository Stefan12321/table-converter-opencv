import cv2

from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from web_table_parser.settings import MEDIA_URL, MEDIA_ROOT


def index(request):
    if request.method == "POST":
        print("POST ", request.POST)
        if 'rotate' in request.POST:
            cv_image = cv2.imread(f'{MEDIA_ROOT}/{request.POST["src"].split("/")[-1]}')
            cv_image = cv2.rotate(cv_image, cv2.ROTATE_90_CLOCKWISE)
            saved_image = f'{MEDIA_ROOT}/saved_image.png'
            print('saved image: ', saved_image)
            cv2.imwrite(saved_image, cv_image)
            return render(request, 'view/index.html', context={'src': f'{MEDIA_URL}/saved_image.png'})
        if 'input-b1' in request.FILES:
            upload = request.FILES['input-b1']
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            return render(request, 'view/index.html', context={'src': f'{MEDIA_URL}{file}'})
        elif 'src' in request.POST:
            return render(request, 'view/index.html', context={'src': request.POST['src']})

    return render(request, 'view/index.html')
