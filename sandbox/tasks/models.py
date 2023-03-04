from django.db import models


class Task(models.Model):
    name = models.CharField("name", max_length=50)
    date_added = models.DateTimeField("date added", auto_now_add=True)
    date_completed = models.DateTimeField(
        "date completed", null=True, default=None, blank=True
    )

    def __str__(self):
        return self.name
