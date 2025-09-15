import pytest
from datetime import date
from rest_framework.test import APIClient

from planner.models import Destination, Schedule, ScheduleDestination, User

pytestmark = pytest.mark.django_db


def test_get_schedule_detail_view_with_weather(monkeypatch):
    client = APIClient()
    user = User.objects.create(username="b0b", email="bob@example.com")
    destination = Destination.objects.create(
        city="Berlin",
        country="Germany",
        latitude="52.520000",
        longitude="13.405000",
    )
    schedule = Schedule.objects.create(name="Germany Trip", user=user)
    ScheduleDestination.objects.create(
        schedule=schedule,
        destination=destination,
        order=1,
        date=date.today(),
    )

    mocked_weather = {"date": date.today().isoformat(), "temp_min": 10.0}

    def _mock_fetch_weather(latitude: str, longitude: str, date: date) -> dict:
        return mocked_weather

    monkeypatch.setattr("planner.views.fetch_weather", _mock_fetch_weather)

    res = client.get(f"/api/schedules/{schedule.id}/")
    assert res.status_code == 200, res.data
    body = res.json()
    assert body["id"] == schedule.id
    assert body["name"] == "Germany Trip"
    assert len(body["destinations"]) == 1
    assert body["destinations"][0]["destination"]["id"] == destination.id
    assert body["destinations"][0]["weather"] == mocked_weather
