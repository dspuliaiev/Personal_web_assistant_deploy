from django.db import models
from django.contrib.auth.models import User

from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=25, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return f"{self.name}"


class File(models.Model):
    title = models.CharField(max_length=50)
    url = CloudinaryField(resource_type='')
    name_file = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='file_category')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return f"{self.title}"
