from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from planner.models import Destination

User = get_user_model()


class Command(BaseCommand):
    help = "Load dummy data"

    def handle(self, *args, **options):
        destinations_data = [
            {
                "city": "Paris",
                "country": "France",
                "latitude": "48.8566",
                "longitude": "2.3522",
            },
            {
                "city": "Rome",
                "country": "Italy",
                "latitude": "41.9028",
                "longitude": "12.4964",
            },
            {
                "city": "Barcelona",
                "country": "Spain",
                "latitude": "41.3851",
                "longitude": "2.1734",
            },
            {
                "city": "Amsterdam",
                "country": "Netherlands",
                "latitude": "52.3676",
                "longitude": "4.9041",
            },
            {
                "city": "Prague",
                "country": "Czech Republic",
                "latitude": "50.0755",
                "longitude": "14.4378",
            },
            {
                "city": "Vienna",
                "country": "Austria",
                "latitude": "48.2082",
                "longitude": "16.3738",
            },
            {
                "city": "Copenhagen",
                "country": "Denmark",
                "latitude": "55.6761",
                "longitude": "12.5683",
            },
            {
                "city": "Stockholm",
                "country": "Sweden",
                "latitude": "59.3293",
                "longitude": "18.0686",
            },
        ]

        for dest_data in destinations_data:
            dest = Destination.objects.create(**dest_data)
            self.stdout.write(f"Created destination: {dest}")

        users_data = [
            {
                "username": "alice123",
                "email": "alice@example.com",
                "first_name": "Alice",
                "last_name": "Johnson",
            },
            {
                "username": "b0b",
                "email": "bob@example.com",
                "first_name": "Bob",
                "last_name": "Smith",
            },
            {
                "username": "charlie_the_hitchhiker",
                "email": "charlie@example.com",
                "first_name": "Charlie",
                "last_name": "Brown",
            },
            {
                "username": "princessdiana",
                "email": "diana@example.com",
                "first_name": "Diana",
                "last_name": "Davis",
            },
        ]

        for user_data in users_data:
            user = User.objects.create(**user_data)
            self.stdout.write(f"Created user: {user}")
