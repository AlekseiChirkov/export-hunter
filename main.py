import requests
import eurostat
import comtradeapicall


eurostat_url = "https://ec.europa.eu/eurostat/api/dissemination"
eurostat_comext_url = "https://ec.europa.eu/eurostat/api/comext/dissemination"

url_template = (
    "{host_url}/{service}/{version}/{response_type}/{dataset_code}"
    "?format={format_}&lang={lang}&{filters}"
)

response = requests.get(
    url=url_template.format(
        host_url=eurostat_url,
        service="statistics",
        version="1.0",
        response_type="data",
        dataset_code="nama_10_gdp",
        format_="JSON",
        lang="EN",
        filters="time=2019"
    )
)

# print(response.json())

# toc = eurostat.get_toc_df()

# eurostat.get_toc_df()

# import requests
#
# # Define the API endpoint URL
# api_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/nama_10_gdp"
#
# # Define the CN code you want to use
# cn_code = "C4420"
#
# # Set the API parameters including the CN code
# params = {
#     "filter": f"cn={cn_code}",
#     "format": "json",
# }
#
# # Send the API request
# response = requests.get(api_url, params=params)
#
# # Check if the request was successful
# if response.status_code == 200:
#     # Process the API response
#     data = response.json()
#     print("eurostat")
#     # ... Perform further actions with the retrieved data
# else:
#     # Handle the API request error
#     print(f"Error: {response.status_code} - {response.text}")

# import requests
#
# # Define the endpoint
# base_url = "https://comtradeapi.un.org/data/v1/get"
#
# # Define the parameters
# typeCode = "C"  # Type of trade (C for commodities)
# freqCode = "A"  # Frequency (A for annual)
# clCode = "HS"  # Classification
#
# # Construct the URL
# url = f"{base_url}/{typeCode}/{freqCode}/{clCode}"
#
# # Optional parameters
# params = {
#     "reporterCode": "826",  # Reporter
#     "period": "2020",  # Periods
#     "partnerCode": "0",  # Partner
#     "cmdCode": "AG2",  # Commodity Code
#     "flowCode": "all",  # Trade flow
#     "includeDesc": "true",  # Include descriptions
# }
#
# # Make the request
# response = requests.get(url, params=params)
#
# # Check the status code
# if response.status_code == 200:
#     # Parse the response to JSON
#     data = response.json()
#     print(data)
# else:
#     print(f"Request failed with status code {response.status_code}")
#

# import comtradeapicall
#
# subscription_key = '42214a2516f64e869ece33dd9a9dd2bb'
#
#
# # Define the parameters
# typeCode = "C"  # Type of trade (C for commodities)
# freqCode = "A"  # Frequency (A for annual)
# clCode = "HS"  # Classification
# period = "2020"  # Periods
# reporterCode = "826"  # Reporter
# cmdCode = "AG2"  # Commodity Code
# flowCode = "all"  # Trade flow
# partnerCode = "0"  # Partner
# partner2Code = None  # Secondary partner
# customsCode = None  # Customs or statistical procedure
# motCode = None  # Mode of transport
# maxRecords = 500  # Maximum records
# format_output = "JSON"  # Format
# includeDesc = True  # Include descriptions
#
# preview = comtradeapicall.previewFinalData(
#     typeCode=typeCode,
#     freqCode=freqCode,
#     clCode=clCode,
#     period=period,
#     reporterCode=reporterCode,
#     cmdCode=cmdCode,
#     flowCode=flowCode,
#     partnerCode=partnerCode,
#     partner2Code=partner2Code,
#     customsCode=customsCode,
#     motCode=motCode,
#     maxRecords=maxRecords,
#     format_output=format_output,
#     includeDesc=includeDesc
# )
# print(preview)

#
# # Make the request
# data = comtradeapicall.getFinalData(
#     subscription_key=subscription_key,
#     typeCode=typeCode,
#     freqCode=freqCode,
#     clCode=clCode,
#     period=period,
#     reporterCode=reporterCode,
#     cmdCode=cmdCode,
#     flowCode=flowCode,
#     partnerCode=partnerCode,
#     partner2Code=partner2Code,
#     customsCode=customsCode,
#     motCode=motCode,
#     maxRecords=maxRecords,
#     format_output=format_output,
#     includeDesc=includeDesc
# )
#
# print(data)


mydf = comtradeapicall.previewFinalData(typeCode='C', freqCode='M', clCode='HS', period='202205',
                                        reporterCode='36', cmdCode='91', flowCode='M', partnerCode=None,
                                        partner2Code=None,
                                        customsCode=None, motCode=None, maxRecords=500, format_output='JSON',
                                        aggregateBy=None, breakdownMode='classic', countOnly=None, includeDesc=True)
print(mydf)