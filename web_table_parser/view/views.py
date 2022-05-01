from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


def index(request):
    if request.method == "POST":
        print(request.POST)
        print("Files: ", request.FILES)
        upload = request.FILES['input-b1']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        print(file)
    # if request.method == "GET":
    #     if request.user.is_authenticated:
    #         tasks_list = Task.objects.filter(user=request.user.id)
    #         return render(request, 'todolistapp/index.html', {'tasks_list': tasks_list})
    return render(request, 'view/index.html')
