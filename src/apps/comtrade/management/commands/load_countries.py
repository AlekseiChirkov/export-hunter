import requests

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.comtrade.models import Country


class Command(BaseCommand):
    help = "Load HS codes from JSON file into the database"

    @staticmethod
    def read_file_generator(file_path: str) -> dict:
        """
        Method reads file and returns lines one by one
        @param file_path: path to reading file
        @type file_path: str
        @return: list with country data
        @rtype: str
        """

        with open(file_path, "r") as file:
            for line in file:
                country_name, m49_code, iso_alpha3_code = line.split(",")
                country = {
                    "name": country_name,
                    "m49_code": m49_code,
                    "iso_alpha3_code": iso_alpha3_code.replace("\n", "")
                }
                yield country

    @staticmethod
    def create_country_objects(countries: dict) -> Country:
        for country in countries:
            if isinstance(country, dict):
                country_id = country.get("m49_code")
                name = country.get("name", "")
                iso_alpha3_code = country.get("iso_alpha3_code", "")

                if country_id:
                    country_object = Country(
                        id=country_id, name=name,
                        iso_alpha3_code=iso_alpha3_code
                    )
                    yield country_object

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

        try:
            with transaction.atomic():
                file_path = (
                    "/home/scareface/Projects/iTechArt"
                    "/export-hunter/export-hunter/src/source/countries.csv"
                )
                country_objects = self.create_country_objects(
                    self.read_file_generator(file_path)
                )

                if country_objects:
                    Country.objects.bulk_create(list(country_objects))

            self.stdout.write(
                self.style.SUCCESS("Countries loaded successfully")
            )

        except ValueError as e:
            self.stderr.write(self.style.ERROR(f"Error in file reading: {e}"))
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"An unexpected error occurred: {e}")
            )
