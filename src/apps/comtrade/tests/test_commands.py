from io import StringIO
from unittest.mock import patch, Mock, MagicMock, mock_open

from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.management import call_command

from requests.exceptions import RequestException

from apps.comtrade.management.commands.load_countries import Command
from apps.comtrade.models import Country


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


class LoadCountriesTest(TestCase):
    """Class to test load_countries command"""

    @patch(
        "builtins.open", new_callable=mock_open,
        read_data="Country1,001,ABC\nCountry2,002,DEF\n"
    )
    def test_read_file_generator(self, _: MagicMock) -> None:
        """
        Method to testfile reading using generator
        @param _: mocked opened file
        @type _: MagicMock
        @return: Nothing
        @rtype: None
        """

        generator = Command.read_file_generator("mock_file_path")
        countries = list(generator)

        self.assertEqual(len(countries), 2)
        self.assertEqual(countries[0]["name"], "Country1")

    def test_create_county_objects(self) -> None:
        """
        Method tests country objects creation
        @return: Nothing
        @rtype: None
        """

        countries = (
            {"name": "Country1", "m49_code": "001", "iso_alpha3_code": "ABC"},
            {"name": "Country2", "m49_code": "002", "iso_alpha3_code": "DEF"}
        )

        generator = Command.create_country_objects(countries)
        county_objects = list(generator)

        self.assertEqual(len(county_objects), 2)
        self.assertEqual(county_objects[0].id, "001")

    @patch("apps.comtrade.models.Country.objects.bulk_create")
    @patch.object(Command, "create_country_objects")
    @patch.object(Command, "read_file_generator")
    def test_handle(self, mock_read_file_generator: MagicMock,
                    mock_create_country_objects: MagicMock,
                    mock_bulk_create: MagicMock) -> None:
        """
        Method tests that handle processes all data and finishes correctly
        @param mock_read_file_generator:mocked file reading
        @type mock_read_file_generator: MagicMock
        @param mock_create_country_objects: mocked creation of country objects
        @type mock_create_country_objects: MagicMock
        @param mock_bulk_create: mocked bulk creation
        @type mock_bulk_create: MagicMock
        @return: Nothing
        @rtype:None
        """

        mock_read_file_generator.return_value = (
            {"name": "Country1", "m49_code": "001", "iso_alpha3_code": "ABC"}
        )
        mock_create_country_objects.return_value = [
            Country(id="001", name="Country1", iso_alpha3_code="ABC"),
        ]

        out = StringIO()
        call_command('load_countries', stdout=out)

        self.assertIn('Countries loaded successfully', out.getvalue())

    @patch("apps.comtrade.models.Country.objects.bulk_create")
    @patch.object(Command, "create_country_objects")
    @patch.object(Command, "read_file_generator")
    def test_handle_with_exceptions(self, mock_read_file_generator: MagicMock,
                                    mock_create_country_objects: MagicMock,
                                    mock_bulk_create: MagicMock) -> None:
        """
        Method tests that handle processes all data and finishes correctly
        @param mock_read_file_generator:mocked file reading
        @type mock_read_file_generator: MagicMock
        @param mock_create_country_objects: mocked creation of country objects
        @type mock_create_country_objects: MagicMock
        @param mock_bulk_create: mocked bulk creation
        @type mock_bulk_create: MagicMock
        @return: Nothing
        @rtype:None
        """

        mock_read_file_generator.side_effect = ValueError

        err = StringIO()
        call_command('load_countries', stderr=err)

        self.assertIn('Error in file reading', err.getvalue())

        mock_read_file_generator.side_effect = Exception

        err = StringIO()
        call_command('load_countries', stderr=err)
        self.assertIn('An unexpected error occurred', err.getvalue())
