from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from works import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("visitor-heartbeat/", views.visitor_heartbeat, name="visitor_heartbeat"),
    path("login/", auth_views.LoginView.as_view(template_name="works/login.html", redirect_authenticated_user=True), name="admin_login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("manage/", views.manage_works, name="manage_works"),
    path("manage/create/", views.create_works, name="create_works"),
    path("manage/stats/", views.manage_stats, name="manage_stats"),
    path("manage/<int:pk>/photos/add/", views.add_work_photos, name="add_work_photos"),
    path("manage/<int:pk>/edit/", views.edit_work, name="edit_work"),
    path("manage/<int:pk>/delete/", views.delete_work, name="delete_work"),
    path("work/<slug:slug>/", views.work_detail, name="work_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
