import requests
from django.db.models import QuerySet, Q

from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.comtrade.models import HSCode
from apps.comtrade.serializers import HSCodeSerializer


class HSCodeListView(generics.ListAPIView):
    """Class to get list of HS codes"""

    serializer_class = HSCodeSerializer

    def get_queryset(self) -> QuerySet:
        """
        Method returns filtered data for autocomplete on frontend input field
        @return: django.db.models.Queryset
        @rtype: QuerySet
        """

        queryset = HSCode.objects.all()
        query = self.request.query_params.get("query", None)

        if query:
            queryset = queryset.filter(Q(id__icontains=query))

        return queryset
