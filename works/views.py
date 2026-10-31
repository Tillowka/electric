from datetime import timedelta

from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import Count
from django.utils import timezone
from django.forms import formset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import AddPhotosForm, WorkForm, WorkImageFormSet
from .models import SiteVisitor, Work, WorkImage

def home(request):
    works = Work.objects.all().prefetch_related("images")
    return render(request, "works/home.html", {"works": works})

def work_detail(request, slug):
    work = get_object_or_404(Work.objects.prefetch_related("images"), slug=slug)
    return render(request, "works/work_detail.html", {"work": work})

@staff_member_required
def manage_works(request):
    return render(request, "works/manage_list.html", {"works": Work.objects.annotate(photo_count=Count("images")).all()})

@staff_member_required
def create_works(request):
    FormSet = formset_factory(WorkForm, extra=1, can_delete=False)
    if request.method == "POST":
        formset = FormSet(request.POST, request.FILES, prefix="works")
        valid_forms = [f for f in formset if f.has_changed()]
        if formset.is_valid() and valid_forms:
            with transaction.atomic():
                for form in valid_forms:
                    form.save()
            messages.success(request, f"Добавлено объектов: {len(valid_forms)}.")
            return redirect("manage_works")
        if not valid_forms:
            messages.error(request, "Заполните хотя бы одну карточку объекта.")
    else:
        formset = FormSet(prefix="works")
    return render(request, "works/manage_create.html", {"formset": formset})

@staff_member_required
def edit_work(request, pk):
    work = get_object_or_404(Work, pk=pk)
    if request.method == "POST":
        form = WorkForm(request.POST, request.FILES, instance=work)
        images = WorkImageFormSet(request.POST, instance=work, prefix="images")
        if form.is_valid() and images.is_valid():
            with transaction.atomic():
                form.save()
                images.save()
            messages.success(request, "Объект обновлён.")
            return redirect("manage_works")
    else:
        form = WorkForm(instance=work)
        images = WorkImageFormSet(instance=work, prefix="images")
    return render(request, "works/manage_edit.html", {"work": work, "form": form, "images": images})


@staff_member_required
def add_work_photos(request, pk):
    work = get_object_or_404(Work, pk=pk)
    if request.method == "POST":
        form = AddPhotosForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data["images"]
            first_order = work.images.count()
            with transaction.atomic():
                for index, image in enumerate(files, start=first_order):
                    caption = request.POST.get(f"caption_{index - first_order}", "").strip()[:220]
                    WorkImage.objects.create(work=work, image=image, caption=caption, order=index)
            messages.success(request, f"Добавлено фотографий: {len(files)}.")
            return redirect("manage_works")
    else:
        form = AddPhotosForm()
    return render(request, "works/manage_photos_add.html", {"work": work, "form": form})


@staff_member_required
def manage_stats(request):
    User = get_user_model()
    now = timezone.now()
    online_since = now - timedelta(minutes=2)
    context = {
        "works_count": Work.objects.count(),
        "photos_count": WorkImage.objects.count(),
        "users_count": User.objects.count(),
        "active_users_count": User.objects.filter(is_active=True).count(),
        "staff_users_count": User.objects.filter(is_staff=True, is_active=True).count(),
        "visitors_total": SiteVisitor.objects.count(),
        "visitors_online": SiteVisitor.objects.filter(last_seen__gte=online_since).count(),
    }
    return render(request, "works/manage_stats.html", context)


def visitor_heartbeat(request):
    """Heartbeat endpoint; middleware refreshes this browser's last_seen timestamp."""
    online_since = timezone.now() - timedelta(minutes=2)
    return JsonResponse({
        "online": SiteVisitor.objects.filter(last_seen__gte=online_since).count(),
        "total": SiteVisitor.objects.count(),
    })

@staff_member_required
@require_POST
def delete_work(request, pk):
    work = get_object_or_404(Work, pk=pk)
    title = work.title
    work.delete()  # related images are deleted by CASCADE
    messages.success(request, f"Объект «{title}» и связанные с ним фотографии удалены.")
    return redirect("manage_works")
