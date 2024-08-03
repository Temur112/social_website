import requests
from django import forms
from django.core.files.base import ContentFile
from images.models import Image


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        # widgets = {
        #     'url': forms.HiddenInput
        # }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError("Please enter a valid image extension")
        return url

    def save(self, commit=True, force_insert=False, force_update=False):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = self.cleaned_data['title']
        extension = image_url.split('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        response = requests.get(image_url)
        image.image.save(
            image_name,
            ContentFile(response.content),
            save=False
        )
        if commit:
            image.save()
        return image
