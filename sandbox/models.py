from django.db import models


class Task(models.Model):
    name = models.CharField("name", max_length=50)
    date_added = models.DateTimeField("date added", auto_now_add=True)
    date_completed = models.DateTimeField("date completed", null=True, default=None, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=192)
    date_published = models.DateField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("sandbox.Author", on_delete=models.CASCADE, related_name="books")

    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=192)

    def __str__(self) -> str:
        return self.name
