import sys

import requests
import comtradeapicall

sub_key = "42214a2516f64e869ece33dd9a9dd2bb"

mydf = comtradeapicall.getMetadata(
    subscription_key=sub_key, typeCode='C', freqCode='M', clCode='HS',
    period='202205', reporterCode=None, showHistory=True
)

mydf = comtradeapicall.getFinalData(
    subscription_key=sub_key, typeCode='C', freqCode='M', clCode='HS',
    period='202205', reporterCode=None, partnerCode=None,
    customsCode=None, flowCode=None, cmdCode="350220", partner2Code=None,
    motCode=None
)
print(mydf)



# url = (
#     "https://comtradeapi.un.org/data/v1/get/C/A/HS"
# )
#
#
# headers = {
#     "Ocp-Apim-Subscription-Key": sub_key,
#     "Cache-Control": "no-cache"
# }

# response = requests.get(
#     url + "?cmdCode=350220&aggregateBy=cmdCode&maxRecords=10",
#     headers=headers
# )
#
# print(response.text)

# response_size = sys.getsizeof(response.json())
#
# print(f"Response size: {response_size} bytes")