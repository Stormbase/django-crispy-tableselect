from django.http import HttpResponse


def index(request):
    return HttpResponse(
        f"This is the django_tableselect boilerplate view on {request.get_full_path()}"
    )
