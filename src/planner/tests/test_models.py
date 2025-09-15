import pytest
from decimal import Decimal
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from planner.models import Destination, Schedule, ScheduleDestination

User = get_user_model()
pytestmark = pytest.mark.django_db


def test_destination_creation():
    destination = Destination.objects.create(
        city="Paris",
        country="France",
        latitude=Decimal("48.8566"),
        longitude=Decimal("2.3522"),
    )
    assert destination.city == "Paris"
    assert destination.country == "France"


def test_destination_unique_constraint():
    Destination.objects.create(city="Paris", country="France")
    with pytest.raises(IntegrityError):
        Destination.objects.create(city="Paris", country="France")


def test_user_creation():
    user = User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.check_password("testpass123")


def test_schedule_creation():
    user = User.objects.create_user(username="testuser")
    schedule = Schedule.objects.create(name="Summer Vacation", user=user)
    assert schedule.name == "Summer Vacation"
    assert schedule.user == user


def test_schedule_destination_creation():
    user = User.objects.create_user(username="testuser")
    schedule = Schedule.objects.create(name="Test Trip", user=user)
    destination = Destination.objects.create(
        city="Paris",
        country="France",
        latitude=Decimal("48.8566"),
        longitude=Decimal("2.3522"),
    )
    schedule_dest = ScheduleDestination.objects.create(
        schedule=schedule, destination=destination, order=1
    )

    assert schedule_dest.schedule == schedule
    assert schedule_dest.destination == destination
    assert schedule_dest.order == 1
