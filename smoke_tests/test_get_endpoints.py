import requests


def test_list_schedules():
    response = requests.get("http://localhost:8000/api/schedules/")
    assert response.status_code == 200


def test_not_found():
    response = requests.get("http://localhost:8000/doesnotexist")
    assert response.status_code == 404


def test_swagger_docs():
    response = requests.get("http://localhost:8000/api/schema/swagger-ui/")
    assert response.status_code == 200


def test_openapi_docs():
    response = requests.get("http://localhost:8000/api/schema/")
    assert response.status_code == 200
