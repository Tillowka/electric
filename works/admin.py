from django.contrib import admin
from .models import Work, WorkImage


class WorkImageInline(admin.TabularInline):
    model = WorkImage
    extra = 1
    fields = ("image", "caption", "order")


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "order", "created_at")
    list_filter = ( "completed_on",)
    list_editable = ( "order",)
    search_fields = ("title", "short_description", "description", "location")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [WorkImageInline]
    fieldsets = (
        ("Основная информация", {
            "fields": ("title", "slug", "short_description", "description")
        }),
        ("Изображения и детали", {
            "fields": ("cover", "location", "completed_on")
        }),
        ("Публикация", {
            "fields": ( "order",)
        }),
    )


@admin.register(WorkImage)
class WorkImageAdmin(admin.ModelAdmin):
    list_display = ("work", "caption", "order")
    list_filter = ("work",)

