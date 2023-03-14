from django.urls import path
from tasks import views

urlpatterns = ([path("table/", views.TaskTableView.as_view(), name="table"), path("bulk/", views.BulkCompleteTaskView.as_view(), name="bulk-complete")], "tasks")
