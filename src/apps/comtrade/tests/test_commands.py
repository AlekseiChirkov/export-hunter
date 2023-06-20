from io import StringIO
from unittest.mock import patch, Mock, MagicMock

from django.core.management import call_command
from django.test import TestCase
from requests.exceptions import RequestException


class LoadHSCodeCommandTestCase(TestCase):

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
