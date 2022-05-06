import cv2

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from web_table_parser.settings import MEDIA_URL, MEDIA_ROOT
from .converter import parse_pic_to_excel_data


def index(request, lang):
    langauge_list = ['rus', 'eng', 'ukr']
    print("GET ", request.GET)
    if request.method == "POST":
        print("POST ", request.POST)
        if 'rotate' in request.POST:
            image = request.POST["src"].split("/")[-1]
            cv_image = cv2.imread(f'{MEDIA_ROOT}/{image}')
            cv_image = cv2.rotate(cv_image, cv2.ROTATE_90_CLOCKWISE)
            saved_image = f'{MEDIA_ROOT}/{image}'
            print('saved image: ', saved_image)
            cv2.imwrite(saved_image, cv_image)
            return render(request, 'view/index.html', context={'src': f'{MEDIA_URL}{request.POST["src"].split("/")[-1]}',
                                                               'langauge': langauge_list,
                                                               'lang': lang})
        if 'scan' in request.POST:
            image = request.POST["src"].split("/")[-1]
            cv_image = cv2.imread(f'{MEDIA_ROOT}/{image}')
            data, cv_image = parse_pic_to_excel_data(cv_image)
            saved_image = f'{MEDIA_ROOT}/saved_image.png'
            cv2.imwrite(saved_image, cv_image)
            return render(request, 'view/index.html', context={'src': f'{MEDIA_URL}/saved_image.png',
                                                               'langauge': langauge_list,
                                                               'lang': lang})
        if 'input-b1' in request.FILES:
            upload = request.FILES['input-b1']
            fss = FileSystemStorage()
            file = fss.save(upload.name, upload)
            return render(request, 'view/index.html', context={'src': f'{MEDIA_URL}{file}',
                                                               'langauge': langauge_list,
                                                               'lang': lang})
        elif 'src' in request.POST:
            return render(request, 'view/index.html', context={'src': request.POST['src'],
                                                               'langauge': langauge_list,
                                                               'lang': lang})

    return render(request, 'view/index.html', context={'langauge': langauge_list,
                                                       'lang': lang})
