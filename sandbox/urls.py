from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.urls import reverse_lazy
from tasks.urls import urlpatterns as tasks_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include(tasks_urlpatterns, namespace="tasks")),
    path("", RedirectView.as_view(url=reverse_lazy('tasks:bulk-complete'))),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
