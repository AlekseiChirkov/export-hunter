from django.urls import path

from apps.comtrade import views

app_name = "comtrade"


urlpatterns = [
    path("hs-codes/",
         views.HSCodeListView.as_view(), name="hs_codes_list"),
    path("countries/",
         views.CountryListView.as_view(), name="countries_list"),
]
