import requests
import re


# agency_id = "ESTAT"
api_base_uri = "https://ec.europa.eu/eurostat/api/dissemination"
# async_endpoint = "https://ec.europa.eu/eurostat/api/dissemination/1.0/async/async.wadl"
# sdmx_2_1_endpoint = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/sdmx-rest.wadl"
# sdmx_2_1 = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1"
# statistics_endpoint = "{api_base_uri}/statistics/1.0/data/{dataset_name}"


def save_xml_file(xml_text: str, file_name: str) -> None:
    with open(file_name, "w") as file:
        file.write(xml_text)


def get_statistics():
    statistics_endpoint = "{api_base_uri}/statistics/1.0/data/{dataset_name}"
    res = requests.get(statistics_endpoint.format(
        api_base_uri=api_base_uri, dataset_name="apro_mk_fatprot"
    ))
    print(res.json())


# TODO: FIRST request to get concept scheme
# response = requests.get("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/conceptscheme/ESTAT/all?detail=allstubs&completestub=true")
# print(response.text)

# TODO: SECOND request to get categorisation
# res = requests.get("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/categorisation/ESTAT/all")
# print(res.text)

# Assuming you have the XML string in the 'xml_string' variable

# Regular expression pattern to match the id attribute
# pattern = r'id="(?!ESTAT)([A-Z_]+)"'
#
# # Find all matches using the pattern
# matches = re.findall(pattern, res.text)
#
# with open("categories.txt", "w") as file:
#     # Write each match to the file
#     for match in set(matches):
#         file.write(match + "\n")