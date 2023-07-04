from django.core.management.base import BaseCommand

from apps.comtrade.models import Region


class Command(BaseCommand):
    help = "Load regions into the database"

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

        regions = (
            Region(id="africa", name="Africa"),
            Region(id="america", name="America"),
            Region(id="asia", name="Asia"),
            Region(id="europe", name="Europe"),
            Region(id="oceania", name="Oceania"),
        )
        Region.objects.bulk_create(regions)

        self.stdout.write(self.style.SUCCESS("Regions loaded successfully"))
