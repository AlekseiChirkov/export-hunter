import requests

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.comtrade.models import HSCode


class Command(BaseCommand):
    help = "Load HS codes from JSON file into the database"

    @staticmethod
    def create_hs_code_objects(hs_codes: dict) -> HSCode:
        for hs_code in hs_codes:
            if isinstance(hs_code, dict):
                code = hs_code.get("id")
                description = hs_code.get("text", "")

                if code:
                    hs_code_object = HSCode(id=code, description=description)
                    yield hs_code_object

    def handle(self, *args, **options) -> None:
        """
        Handle command to load HS codes from JSON file to database
        @param args: list of additional arguments
        @type args: list
        @param options: dict of keyword arguments
        @type options: dict
        @return: Command returns nothing
        @rtype: None
        """

        url = "https://comtradeapi.un.org/files/v1/app/reference/HS.json"

        try:
            response = requests.get(url, stream=True)

            # Check if the request was successful
            response.raise_for_status()

            hs_codes = response.json()

            with transaction.atomic():
                hs_code_objects = self.create_hs_code_objects(hs_codes["results"])

                # Insert remaining items
                if hs_code_objects:
                    HSCode.objects.bulk_create(list(hs_code_objects))

            self.stdout.write(self.style.SUCCESS("HS codes loaded successfully"))

        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f"Network error: {e}"))
        except ValueError as e:
            self.stderr.write(self.style.ERROR(f"Error decoding JSON: {e}"))
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"An unexpected error occurred: {e}"))

