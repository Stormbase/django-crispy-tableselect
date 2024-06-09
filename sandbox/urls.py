from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from sandbox import views

tasks_urls = (
    [
        path("table/", views.TaskTableView.as_view(), name="table"),
        path("bulk/", views.BulkCompleteTaskView.as_view(), name="bulk-complete"),
    ],
    "tasks",
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", include(tasks_urls, namespace="tasks")),
    # path("books/", include(books_urls, namespace="books")),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
