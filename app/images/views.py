from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from images.forms import ImageForm


# Create your views here.

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image successfully created')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageForm(data=request.GET)
    return render(request, 'images/image/image_create.html', {'form': form, 'section': 'images'})
