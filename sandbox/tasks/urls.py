from django.urls import path
from tasks.views import TaskTableView

urlpatterns = ([path("table/", TaskTableView.as_view(), name="table")], "tasks")
