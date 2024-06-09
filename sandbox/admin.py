from django.contrib import admin

from sandbox.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "date_added")


admin.site.register(Task, TaskAdmin)
