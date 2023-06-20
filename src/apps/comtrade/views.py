from django.db.models import QuerySet, Q

from rest_framework import generics

from apps.comtrade import models
from apps.comtrade import serializers


class HSCodeListView(generics.ListAPIView):
    """Class to get list of HS codes"""

    serializer_class = serializers.HSCodeSerializer

    def get_queryset(self) -> QuerySet:
        """
        Method returns filtered data for autocomplete on frontend input field
        @return: django.db.models.Queryset
        @rtype: QuerySet
        """

        queryset = models.HSCode.objects.all().order_by("id")
        query = self.request.query_params.get("query", None)

        if query:
            queryset = queryset.filter(Q(id__icontains=query))

        return queryset


class CountryListView(generics.ListAPIView):
    """Class to get list of Countries"""

    serializer_class = serializers.CountrySerializer

    def get_queryset(self) -> QuerySet:
        """
        Method returns filtered countries data for autocomplete on
        frontend input field
        @return: django.db.models.Queryset
        @rtype: QuerySet
        """

        queryset = models.Country.objects.all().order_by("name")
        query = self.request.query_params.get("query", None)

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(iso_alpha3_code__icontains=query)
            )

        return queryset
