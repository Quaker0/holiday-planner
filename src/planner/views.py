from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .models import Destination, Schedule
from .serializers import (
    DestinationSerializer,
    ScheduleCreateSerializer,
    ScheduleDetailSerializer,
)
from .weather_api import fetch_weather


class ScheduleListCreateView(APIView):
    serializer_class = ScheduleCreateSerializer

    @extend_schema(operation_id="schedules_list")
    def get(self, request):
        schedules = Schedule.objects.all()
        serializer = ScheduleDetailSerializer(
            schedules, many=True, context={"fetch_weather": fetch_weather}
        )
        return Response(serializer.data)

    @extend_schema(operation_id="schedules_create")
    def post(self, request):
        serializer = ScheduleCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        schedule = serializer.save()
        out = ScheduleDetailSerializer(
            schedule, context={"fetch_weather": fetch_weather}
        )
        return Response(out.data, status=status.HTTP_201_CREATED)


class ScheduleDetailView(APIView):
    serializer_class = ScheduleDetailSerializer

    @extend_schema(operation_id="schedules_get")
    def get(self, request, pk: int):
        schedule = get_object_or_404(Schedule.objects.all(), pk=pk)
        serializer = ScheduleDetailSerializer(
            schedule,
            context={"fetch_weather": fetch_weather},
        )
        return Response(serializer.data)


class DestinationListCreateView(APIView):
    serializer_class = DestinationSerializer

    @extend_schema(operation_id="destinations_list")
    def get(self, request):
        destinations = Destination.objects.all()
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data)
