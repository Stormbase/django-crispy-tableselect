from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=192)
    date_published = models.DateField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        "testapp.Author", on_delete=models.CASCADE, related_name="books"
    )

    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=192)

    def __str__(self) -> str:
        return self.name
