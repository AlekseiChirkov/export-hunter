from django.test import TestCase

from apps.comtrade.models import HSCode, Country


class HSCodeModelTest(TestCase):
    """Class to test HSCode model"""

    def test_string_representation(self) -> None:
        """
        Method tests string representation for HSCode model
        @return: Nothing
        @rtype: None
        """

        hs_code = HSCode.objects.create(id="AABB11", description="Test object")

        self.assertEqual(str(hs_code), "AABB11")


class CountryModelTest(TestCase):
    """Class to test Country model"""

    def test_string_representation(self) -> None:
        """
        Method tests string representation for Country model
        @return: Nothing
        @rtype: None
        """

        country = Country.objects.create(
            id=1, name="Kyrgyzstan", iso_alpha3_code="KGZ"
        )

        self.assertEqual(str(country), "Kyrgyzstan")
