from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Image
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


def image_detail(request, image_id, slug=None):
    image = get_object_or_404(Image, id=image_id, slug=slug)
    return render(
        request,
        'images/image/image_detail.html',
        {'image': image, 'section': 'images'}
    )

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('image_id')
    actions = request.POST.get('action')
    if image_id and actions:
        try:
            image = Image.objects.get(id=image_id)
            if actions == 'like':
                image.user_like.add(request.user)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})
