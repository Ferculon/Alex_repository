from django import forms
from django.core import validators

from .models import Product
from django import forms


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'discount', 'description', 'preview'

    images = forms.ImageField(
        widget=forms.ClearableFileInput(),
    )

    # данное поле в форме с widget позволяет загружать сразу несколько картинок разом
    # images = forms.ImageField(
    #     widget=forms.ClearableFileInput(
    #         attrs={'multiple': True},),
    # )

# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(max_digits=8, decimal_places=2, min_value=1)
#     description = forms.CharField(label='Product description',
#                                   validators=[validators.RegexValidator(
#                                       regex=r'great',
#                                       message='field must contain "great"',
#                                   )],
#                                   widget=forms.Textarea(attrs={
#                                       'cols': 50,
#                                       'rows': 6,
#                                   }
#                                   ))
#     discount = forms.IntegerField(min_value=1, max_value=15)


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
