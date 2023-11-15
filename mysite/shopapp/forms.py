from django import forms
from django.core import validators
from .models import Product
from django.contrib.auth.models import Group


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount', 'preview'

    images = MultipleFileField()


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = 'name',

# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100, label='Name of product')
#     price = forms.DecimalField(min_value=1, max_value=100000, decimal_places=2)
#     description = forms.CharField(
#         label='Description of product',
#         widget=forms.Textarea(attrs={'rows': 5, 'cols': 10}),
#         validators=[validators.RegexValidator(
#             regex=r'great',
#             message='Field must contain word GREAT'
#         )],
#     )
#


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()
