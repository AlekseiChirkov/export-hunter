from django.test import TestCase

from apps.comtrade.models import HSCode, Country, Region, SkipDay


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


class RegionModelTest(TestCase):
    """Class to test Region model"""

    def test_string_representation(self) -> None:
        """
        Method tests string representation for Region model
        @return: Nothing
        @rtype: None
        """

        region = Region.objects.create(id='oceania', name='Oceania')

        self.assertEqual(str(region), 'Oceania')


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


class SkipDayModelTest(TestCase):
    """Class to test SkipDay model"""

    def test_string_representation(self) -> None:
        """
        Method tests string representation for SkipDay model
        @return: Nothing
        @rtype: None
        """

        skip_day = SkipDay.objects.create()

        self.assertEqual(str(skip_day), "Skipped 2 days")

    def test_load(self) -> None:
        """
        Method tests load method successfully gets or creates object
        @return: Nothing
        @rtype: None
        """

        skip_day = SkipDay.load()

        self.assertEqual(skip_day.amount, 2)
        self.assertEqual(skip_day.pk, 1)

