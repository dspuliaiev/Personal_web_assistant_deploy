from django.forms import ModelForm, CharField, TextInput
from cloudinary.models import CloudinaryField

from .models import Category, File


class CategoryForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True,
                     widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'})
    )

    class Meta:
        model = Category
        fields = ['name']


class FileForm(ModelForm):
    title = CharField(max_length=50, widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}))
    url = CloudinaryField(resource_type='')

    class Meta:
        model = File
        fields = ['title', 'url']
        exclude = ['categories']
