from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Destination, Schedule, ScheduleDestination, User


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = [
            "id",
            "city",
            "country",
            "latitude",
            "longitude",
        ]
        read_only_fields = [
            "id",
            "city",
            "country",
            "latitude",
            "longitude",
        ]


class ScheduleDestinationCreateSerializer(serializers.ModelSerializer):
    destination_id = serializers.PrimaryKeyRelatedField(
        source="destination",
        queryset=Destination.objects.all(),
        write_only=True,
    )

    class Meta:
        model = ScheduleDestination
        fields = [
            "destination_id",
            "date",
        ]


class ScheduleCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source="user", queryset=User.objects.all(), write_only=True
    )
    destinations = ScheduleDestinationCreateSerializer(many=True, required=False)

    class Meta:
        model = Schedule
        fields = [
            "id",
            "name",
            "user_id",
            "created_at",
            "destinations",
        ]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        destinations_data = validated_data.pop("destinations", [])
        schedule = Schedule.objects.create(**validated_data)

        for index, item in enumerate(destinations_data, start=1):
            ScheduleDestination.objects.create(
                schedule=schedule,
                order=index,
                **item,
            )
        return schedule


class ScheduleDestinationWithWeatherSerializer(serializers.ModelSerializer):
    destination = DestinationSerializer(read_only=True)
    weather = serializers.SerializerMethodField()

    class Meta:
        model = ScheduleDestination
        fields = [
            "id",
            "order",
            "date",
            "destination",
            "weather",
        ]
        read_only_fields = ["id"]

    @extend_schema_field(serializers.JSONField())
    def get_weather(self, obj):
        fetch_weather = self.context["fetch_weather"]
        return fetch_weather(
            latitude=str(obj.destination.latitude),
            longitude=str(obj.destination.longitude),
            date=obj.date,
        )


class ScheduleDetailSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    destinations = ScheduleDestinationWithWeatherSerializer(
        source="schedule_destinations", many=True, read_only=True
    )

    class Meta:
        model = Schedule
        fields = [
            "id",
            "name",
            "user",
            "created_at",
            "destinations",
        ]
        read_only_fields = ["id", "created_at"]
