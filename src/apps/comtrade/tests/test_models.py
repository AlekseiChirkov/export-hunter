from django.test import TestCase

from apps.comtrade.models import HSCode


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
