from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Work, WorkImage


@receiver(pre_delete, sender=Work)
def delete_work_files(sender, instance, **kwargs):
    # Remove uploaded files from storage as well as their database rows.
    if instance.cover:
        instance.cover.delete(save=False)


@receiver(pre_delete, sender=WorkImage)
def delete_work_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
