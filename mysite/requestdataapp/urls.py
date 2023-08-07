from django.urls import path
from .views import process_get_view, user_form, upload_file

app_name = 'requestdataapp'

urlpatterns = [
    path('get/', process_get_view, name='get-view'),
    path('bio/', user_form, name='user_bio'),
    path('upload/', upload_file, name='upload_file'),
]
