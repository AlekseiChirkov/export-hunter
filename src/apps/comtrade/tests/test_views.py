from django.urls import reverse

from rest_framework.test import APITestCase

from apps.comtrade.models import HSCode
from apps.comtrade.views import HSCodeListView


class HSCodeListViewTest(APITestCase):
    """Class to test HSCodeListView"""

    def setUp(self) -> None:
        HSCode.objects.create(id="123", description="Test 1")
        HSCode.objects.create(id="456", description="Test 2")
        HSCode.objects.create(id="789", description="Test 3")

    def test_matching_query(self) -> None:
        """
        Method tests that data filtered using query
        @return: Nothing
        @rtype: None
        """

        response = self.client.get(
            reverse("comtrade:hs_codes_list"), {"query": "12"}
        )
        response_data = response.data.get("results")

        self.assertEqual(response_data[0].get("id"), "123")

    def test_not_matching_query(self) -> None:
        """
        Method tests that query not match and endpoint returns empty array in
        results
        @return: Nothing
        @rtype: None
        """

        response = self.client.get(
            reverse("comtrade:hs_codes_list"), {"query": "xyz"}
        )
        response_data = response.data.get("results")

        self.assertEqual(len(response_data), 0)

    def test_no_query_parameters(self) -> None:
        """
        Method tests that no query parameters provided and endpoint returns
        all data
        @return: Nothing
        @rtype: None
        """

        response = self.client.get(reverse("comtrade:hs_codes_list"))
        response_data = response.data.get("results")

        self.assertEqual(len(response_data), 3)
