from django.db.models.base import ValidationError
import pytest
from datetime import date
from planner.serializers import DestinationSerializer, ScheduleCreateSerializer
from planner.models import Destination, User

pytestmark = pytest.mark.django_db


def test_destination_create():
    dest = Destination.objects.create(
        city="Paris", country="France", latitude="48.856600", longitude="2.352200"
    )
    data = DestinationSerializer(dest).data
    assert data["city"] == "Paris"
    assert data["country"] == "France"
    assert data["latitude"] == "48.856600"
    assert data["longitude"] == "2.352200"


def test_destination_validation_invalid_longitude():
    with pytest.raises(ValidationError):
        Destination.objects.create(
            city="Paris", country="France", latitude="48.856600", longitude="invalid"
        )


def test_destination_update_with_readonly_fields():
    dest = Destination.objects.create(
        city="Paris", country="France", latitude="48.856600", longitude="2.352200"
    )

    serializer = DestinationSerializer(dest, data={"city": "Not Paris"}, partial=True)
    assert serializer.is_valid(), serializer.errors

    updated_dest = serializer.save()
    assert updated_dest.city == "Paris"


def test_schedule_create():
    user = User.objects.create(username="u1", email="u1@example.com")
    payload = {
        "name": "Trip",
        "user_id": user.id,
        "destinations": [
            {
                "destination_id": Destination.objects.create(city="A", country="X").id,
                "date": date.today(),
            },
            {
                "destination_id": Destination.objects.create(city="B", country="X").id,
                "date": date.today(),
            },
        ],
    }
    serializer = ScheduleCreateSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    schedule = serializer.save()
    orders = [sd.order for sd in schedule.schedule_destinations.all().order_by("order")]
    assert orders == [1, 2]
