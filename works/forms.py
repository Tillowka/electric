from django import forms
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory, formset_factory
from .models import Work, WorkImage

class WorkForm(forms.ModelForm):
    cover = forms.ImageField(validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])], required=False)

    def clean_cover(self):
        cover = self.cleaned_data.get("cover")
        if cover and cover.size > 8 * 1024 * 1024:
            raise ValidationError("Размер обложки не должен превышать 8 МБ.")
        if not cover and not self.instance.pk:
            raise ValidationError("Добавьте главное изображение объекта.")
        return cover

    class Meta:
        model = Work
        fields = ("title", "slug", "short_description", "description", "cover", "location", "completed_on",  "order")
        widgets = {"completed_on": forms.DateInput(attrs={"type": "date"}), "description": forms.Textarea(attrs={"rows": 5})}

class WorkImageForm(forms.ModelForm):
    image = forms.ImageField(validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])], required=False)

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > 8 * 1024 * 1024:
            raise ValidationError("Размер фотографии не должен превышать 8 МБ.")
        if not image and not self.instance.pk:
            raise ValidationError("Выберите фотографию или удалите пустую строку.")
        return image

    class Meta:
        model = WorkImage
        fields = ("image", "caption", "order")

# On the edit page existing photos can be captioned/reordered/deleted, but not uploaded.
WorkImageFormSet = inlineformset_factory(
    Work,
    WorkImage,
    fields=("caption", "order"),
    extra=0,
    can_delete=True,
)
MultiWorkFormSet = formset_factory(WorkForm, extra=1, can_delete=False)


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        if not data:
            return []
        files = data if isinstance(data, (list, tuple)) else [data]
        cleaned = []
        for uploaded in files:
            image = super().clean(uploaded, initial)
            if image.size > 8 * 1024 * 1024:
                raise ValidationError(f"Файл «{image.name}» превышает 8 МБ.")
            cleaned.append(image)
        return cleaned


class AddPhotosForm(forms.Form):
    images = MultipleImageField(
        label="Фотографии",
        required=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"])],
        help_text="Можно выбрать несколько JPG, PNG или WEBP. Максимум 8 МБ на файл.",
    )

    def clean_images(self):
        images = self.cleaned_data["images"]
        if len(images) > 50:
            raise ValidationError("За один раз можно загрузить не более 50 фотографий.")
        return images
