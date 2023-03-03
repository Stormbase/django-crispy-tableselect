from django.urls import reverse


def test_root_view(client):
    url = reverse("django_tableselect:index")
    response = client.get(url)
    assert response.status_code == 200
