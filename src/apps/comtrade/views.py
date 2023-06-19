import requests

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.comtrade.models import HSCode
from apps.comtrade.serializers import HSCodeSerializer


class HSCodeListView(generics.ListAPIView):
    """Class to get list of HS codes"""

    queryset = HSCode.objects.all()
    serializer_class = HSCodeSerializer
