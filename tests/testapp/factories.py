import factory

from . import models


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Author

    name = factory.Faker("name")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Book

    title = factory.Faker("sentence", nb_words=4)
    date_published = factory.Faker("date_this_century")
    author = factory.SubFactory(AuthorFactory)
