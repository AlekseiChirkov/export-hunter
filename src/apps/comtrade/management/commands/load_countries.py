import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.comtrade.models import Region, Country


class Command(BaseCommand):
    help = "Load countries into the database"

    @staticmethod
    def process_countries_by_regions(regions):
        new_regions = {
            "africa": [],
            "america": [],
            "asia": [],
            "europe": [],
            "oceania": [],
        }

        for region in regions:
            for sub_region in region["sub_regions"]:
                for country_data in sub_region:
                    info = country_data.find_all("td")
                    country_name = info[0].text
                    m49_code = info[1].text
                    iso_code = info[2].text
                    country = {
                        "id": m49_code,
                        "name": country_name,
                        "iso_alpha3_code": iso_code,
                        "region": region["name"]
                    }
                    new_regions[region["name"]].append(country)
        return new_regions

    def get_regions_with_countries(self):
        response = requests.get(
            url="https://unstats.un.org/unsd/methodology/m49/",
        )
        soup = BeautifulSoup(response.text, "html.parser")

        table = soup.find("table", {"id": "GeoGroupsENG"})
        oceania = {
            "name": "oceania",
            "sub_regions": [
                table.find_all("tr", {"data-tt-parent-id": "053"}),
                table.find_all("tr", {"data-tt-parent-id": "054"}),
                table.find_all("tr", {"data-tt-parent-id": "057"}),
                table.find_all("tr", {"data-tt-parent-id": "061"}),
            ]
        }
        europe = {
            "name": "europe",
            "sub_regions": [
                table.find_all("tr", {"data-tt-parent-id": "151"}),
                table.find_all("tr", {"data-tt-parent-id": "830"}),
                table.find_all("tr", {"data-tt-parent-id": "154"}),
                table.find_all("tr", {"data-tt-parent-id": "039"}),
                table.find_all("tr", {"data-tt-parent-id": "155"}),
            ]
        }
        asia = {
            "name": "asia",
            "sub_regions": [
                table.find_all("tr", {"data-tt-parent-id": "143"}),
                table.find_all("tr", {"data-tt-parent-id": "030"}),
                table.find_all("tr", {"data-tt-parent-id": "035"}),
                table.find_all("tr", {"data-tt-parent-id": "034"}),
                table.find_all("tr", {"data-tt-parent-id": "145"}),
            ]
        }
        america = {
            "name": "america",
            "sub_regions": [
                table.find_all("tr", {"data-tt-parent-id": "021"}),
                table.find_all("tr", {"data-tt-parent-id": "005"}),
                table.find_all("tr", {"data-tt-parent-id": "013"}),
                table.find_all("tr", {"data-tt-parent-id": "029"}),
            ]
        }
        africa = {
            "name": "africa",
            "sub_regions": [
                table.find_all("tr", {"data-tt-parent-id": "015"}),
                table.find_all("tr", {"data-tt-parent-id": "014"}),
                table.find_all("tr", {"data-tt-parent-id": "017"}),
                table.find_all("tr", {"data-tt-parent-id": "018"}),
                table.find_all("tr", {"data-tt-parent-id": "011"}),
            ]
        }

        regions = [africa, america, asia, europe, oceania]
        regions = self.process_countries_by_regions(regions)
        return regions

    @staticmethod
    def create_country_objects(regions: dict) -> Country:
        for countries in regions.values():
            for country in countries:
                if isinstance(country, dict):
                    country_id = country.get("id")
                    name = country.get("name", "")
                    iso_alpha3_code = country.get("iso_alpha3_code", "")
                    region = country.get("region", "")

                    if country_id:
                        country_object = Country(
                            id=country_id,
                            name=name,
                            iso_alpha3_code=iso_alpha3_code,
                            region=Region.objects.get(id=region)
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
                regions = self.get_regions_with_countries()
                country_objects = list(self.create_country_objects(regions))

                if country_objects:
                    batch_size = 50
                    total_objects = len(country_objects)
                    for index in range(0, total_objects, batch_size):
                        batch = country_objects[index:index+batch_size]
                        Country.objects.bulk_create(batch)

            self.stdout.write(
                self.style.SUCCESS("Countries loaded successfully")
            )

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"An unexpected error occurred: {e}")
            )
