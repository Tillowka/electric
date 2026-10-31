from django.db import models
from django.urls import reverse


class Work(models.Model):
    title = models.CharField("Название объекта", max_length=180)
    slug = models.SlugField("Адрес страницы", unique=True, help_text="Например: dom-v-kokande")
    short_description = models.CharField("Краткое описание для карточки", max_length=260)
    description = models.TextField("Подробное описание работ")
    cover = models.ImageField("Главное изображение", upload_to="works/covers/")
    location = models.CharField("Место / тип объекта", max_length=180, blank=True)
    completed_on = models.DateField("Дата завершения", blank=True, null=True)
    order = models.PositiveIntegerField("Порядок на главной", default=0)
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Объект / работа"
        verbose_name_plural = "Объекты / работы"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("work_detail", kwargs={"slug": self.slug})


class WorkImage(models.Model):
    work = models.ForeignKey(
        Work, on_delete=models.CASCADE, related_name="images",
        verbose_name="Объект"
    )
    image = models.ImageField("Фотография", upload_to="works/gallery/")
    caption = models.CharField("Подпись к фотографии", max_length=220, blank=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Фотография объекта"
        verbose_name_plural = "Фотографии объекта"

    def __str__(self):
        return f"Фото: {self.work.title}"


class SiteVisitor(models.Model):
    """Browser/session-based visitor tracking without storing IP addresses."""
    visitor_key = models.CharField("Идентификатор посетителя", max_length=64, unique=True)
    first_seen = models.DateTimeField("Первое посещение", auto_now_add=True)
    last_seen = models.DateTimeField("Последняя активность", db_index=True)

    class Meta:
        verbose_name = "Посетитель сайта"
        verbose_name_plural = "Посетители сайта"

    def __str__(self):
        return f"Посетитель {self.visitor_key[:8]}"
