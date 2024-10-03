from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseNotFound
import os
from .models import Category, File
from .forms import CategoryForm, FileForm


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            categories = Category.objects.filter(user=request.user)
            new_category = form.save(commit=False)
            is_new_category = True
            for category in categories:
                if new_category.name == category.name:
                    is_new_category = False
                    break
            if is_new_category:
                new_category.user = request.user
                new_category.save()
            return redirect(to='files:categories')
        else:
            return render(request, 'files/category_create.html', {'form': form})

    return render(request, 'files/category_create.html', {'form': CategoryForm()})


@login_required
def categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(
            request, "files/categories.html", {"categories": categories}
        )


@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if category:
        category.delete()
    return redirect('files:categories')


@login_required
def files(request):
    files = File.objects.filter(user=request.user)
    return render(request, "files/files.html", {"files": files})


@login_required
def files_id(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    files = File.objects.filter(user=request.user, category=category_id)
    return render(request, "files/files_id.html", {"files": files, "category": category})


@login_required
def create(request):
    categories = Category.objects.filter(user=request.user)
    context = dict(backend_form=FileForm())
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.name_file = str(request.FILES["url"])
            choice_category = Category.objects.filter(name__in=request.POST.getlist("categories"))
            for category_one in choice_category.iterator():
                new_file.category = Category.objects.get(name=category_one, user=request.user)
            new_file.user = request.user
            new_file.save()
        else:
            render(request, 'files/create.html', {"categories": categories, "backend_form": form})
    return render(request, 'files/create.html', {"categories": categories, "backend_form": FileForm()})


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound


@login_required
def download(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    if file and file.url:
        # Get the URL for the file from Cloudinary.
        download_url = file.url.url

        # Add the "attachment" flag to the URL.
        download_url += "?attachment=true"

        # Redirect the user to the download URL.
        return HttpResponseRedirect(download_url)
    return HttpResponseNotFound('File not found')
