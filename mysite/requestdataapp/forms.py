from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError


class UserBioForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    age = forms.IntegerField(label='Age', min_value=1, max_value=120)
    bio = forms.CharField(label='Biography', widget=forms.Textarea(attrs={
            'cols': 30,
            'rows': 5,
        }
    ))


def validate_file_name(file: InMemoryUploadedFile):
    if file.name and 'virus' in file.name:
        raise ValidationError('File name should not contain "virus"')


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])
