from io import StringIO
from unittest.mock import patch, Mock, MagicMock

from bs4 import BeautifulSoup
from django.test import TestCase
from django.core.management import call_command

from requests.exceptions import RequestException

from apps.comtrade.management.commands.load_countries import Command
from apps.comtrade.models import Country, Region


class LoadHSCodeCommandTestCase(TestCase):
    """Class to test load_hs_codes command"""

    @patch('apps.comtrade.models.HSCode.objects.bulk_create')
    @patch('requests.get')
    def test_successful_data_load(self, mock_get: MagicMock,
                                  mock_bulk_create: MagicMock) -> None:
        """
        Method tests that data successfully loaded
        @param mock_get: mocked get request
        @type mock_get: MagicMock
        @param mock_bulk_create: mocked bulk creation of objects
        @type mock_bulk_create: MagicMock
        @return: Nothing
        @rtype: None
        """

        mock_response = Mock()
        mock_response.json.return_value = {
            "results": [{"id": "123", "text": "example"}]
        }
        mock_get.return_value = mock_response

        out = StringIO()
        call_command('load_hs_codes', stdout=out)

        self.assertIn('HS codes loaded successfully', out.getvalue())

    @patch('requests.get')
    def test_network_error(self, mock_get: MagicMock) -> None:
        """
        Method tests that network error raises
        @param mock_get: mocked get request
        @type mock_get: MagicMock
        @return: Nothing
        @rtype: None
        """

        mock_get.side_effect = RequestException

        err = StringIO()
        call_command('load_hs_codes', stderr=err)

        self.assertIn('Network error', err.getvalue())

    @patch('requests.get')
    def test_json_decoding_error(self, mock_get: MagicMock) -> None:
        """
        Method tests that json decoding error raises ValueError
        @param mock_get: mocked get request
        @type mock_get: MagicMock
        @return: Nothing
        @rtype: None
        """
        mock_response = Mock()
        mock_response.json.side_effect = ValueError
        mock_get.return_value = mock_response

        err = StringIO()
        call_command('load_hs_codes', stderr=err)

        self.assertIn('Error decoding JSON', err.getvalue())

    @patch('requests.get')
    def test_general_exception(self, mock_get: MagicMock) -> None:
        """
        Method tests that Exception raises on unexpected errors
        @param mock_get: mocked get request
        @type mock_get: MagicMock
        @return: Nothing
        @rtype: None
        """

        mock_get.side_effect = Exception

        err = StringIO()
        call_command('load_hs_codes', stderr=err)

        self.assertIn('An unexpected error occurred', err.getvalue())


class LoadRegionsTest(TestCase):
    """Class to test load_regions command"""

    @patch("apps.comtrade.models.Region.objects.bulk_create")
    def test_successful_load_regions(self,
                                     mock_bulk_create: MagicMock) -> None:
        """
        Method tests that regions loaded successfully
        @return: Nothing
        @rtype: None
        """

        out = StringIO()
        call_command('load_regions', stdout=out)

        self.assertIn('Regions loaded successfully', out.getvalue())


class LoadCountryTest(TestCase):
    """Class to test load_country command"""

    def setUp(self) -> None:
        self.command = Command()
        self.region = Region.objects.get_or_create(id="oceania", name="Oceania")

    @patch('requests.get')
    def test_get_regions_with_countries(self, mock_get: MagicMock) -> None:
        """
        Method tests that get_regions_with_countries works correctly
        @param mock_get: Mocked get request
        @type mock_get: MagicMock
        @return: Nothing
        @rtype: None
        """

        mock_get.return_value.text = (
            """
            <table id="GeoGroupsENG">
                <tr data-tt-parent-id="054">
                    <td>Australia</td>
                    <td>036</td>
                    <td>AUS</td>
                </tr>
            </table>
            """
        )

        regions = self.command.get_regions_with_countries()
        self.assertEqual(len(regions["oceania"]), 1)
        self.assertEqual(regions["oceania"][0]["name"], "Australia")

    def test_process_countries_by_regions(self) -> None:
        """
        Method tests processing of countries by regions
        @return: Nothing
        @rtype: None
        """

        html = """
            <tr data-tt-id="012" data-tt-parent-id="015">
                <td>Algeria</td><td style="text-align:right">012</td>
                <td style="text-align:right">DZA</td>
                <td style="text-align:right"> </td>
            </tr>
        """
        soup = BeautifulSoup(html, 'html.parser')

        regions = [
            {
                'name': 'africa',
                'sub_regions': [
                    [soup],
                ]
            },
        ]
        processed = self.command.process_countries_by_regions(regions)
        self.assertEqual(len(processed["africa"]), 1)
        self.assertEqual(processed["africa"][0]['name'], 'Algeria')

    def test_create_country_objects(self) -> None:
        """
        Method tests countries objects creation
        @return: Nothing
        @rtype: None
        """

        regions = {
            "oceania": [
                {
                    "id": "036",
                    "name": "Australia",
                    "iso_alpha3_code": "AUS",
                    "region": "oceania"
                }
            ]
        }
        countries = list(self.command.create_country_objects(regions))
        region = Region.objects.get(id="oceania")
        self.assertEqual(len(countries), 1)
        self.assertEqual(countries[0].name, 'Australia')
        self.assertEqual(countries[0].region, region)

    @patch.object(Command, 'get_regions_with_countries')
    @patch.object(Command, 'create_country_objects')
    def test_handle(self, mock_create_country_objects: MagicMock,
                    mock_get_regions_with_countries: MagicMock) -> None:
        """
        Method tests that command works correctly
        @param mock_create_country_objects: mocked method to create country
        @type mock_create_country_objects: MagicMock
        @param mock_get_regions_with_countries: mocked method to create region
        @type mock_get_regions_with_countries: MagicMock
        @return: Nothing
        @rtype: None
        """

        mock_get_regions_with_countries.return_value = {
            "oceania": [
                {
                    "id": "036",
                    "name": "Australia",
                    "iso_alpha3_code": "AUS",
                    "region": "oceania"
                }
            ]
        }
        mock_create_country_objects.return_value = [
            Country(
                id='036',
                name='Australia',
                iso_alpha3_code='AUS',
                region=Region.objects.get(id="oceania")
            )
        ]

        out = StringIO()
        call_command('load_countries', stdout=out)

        self.assertIn('Countries loaded successfully', out.getvalue())

        err = StringIO()
        call_command('load_countries', stderr=err)

        self.assertIn('An unexpected error occurred', err.getvalue())
