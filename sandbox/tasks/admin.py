from django.contrib import admin
from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "date_added")


admin.site.register(Task, TaskAdmin)
