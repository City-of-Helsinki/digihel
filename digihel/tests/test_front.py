import pytest


@pytest.mark.django_db
def test_front_page(client, home_page):
    response = client.get('/')
    assert response.status_code == 200
    print(response.content)
    assert 'Helsingin kaupunki' in str(response.content)
