from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import UserBioForm, UploadFileForm


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result,
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    form = UserBioForm()
    context = {
        'form': form
    }
    return render(request, 'requestdataapp/user-bio-form.html', context=context)


def upload_file(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # my_file = request.FILES['myfile']
            my_file = form.cleaned_data['file']  # когда используем форму из файла form.py
            fs = FileSystemStorage()
            file_name = fs.save(my_file.name, my_file)
            print('Saved file', file_name)
    else:
        form = UploadFileForm()
    context = {
        'form': form
    }
    return render(request, 'requestdataapp/file-upload.html', context=context)

# реализация без файла forms.py
# def upload_file(request: HttpRequest) -> HttpResponse:
#     if request.method == 'POST' and request.FILES['myfile']:
#         my_file = request.FILES['myfile']
#         fs = FileSystemStorage()
#         file_name = fs.save(my_file.name, my_file) #сохранение имение файла и самого файла
#         print('Saved file', file_name)
#     return render(request, 'requestdataapp/file-upload.html', context=context)
