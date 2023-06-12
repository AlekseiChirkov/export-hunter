import comtradeapicall

sub_key = "42214a2516f64e869ece33dd9a9dd2bb"


selection_criteria = {
    "typeCode": "C",
    "freqCode": "A",
    "clCode": "HS",
    "period": "2022",
    "reporterCode": None,
    "cmdCode": "010229",
    "flowCode": None,
    "partnerCode": None,
    "partner2Code": None,
    "customsCode": None,
    "motCode": None
}

query_options = {
    "maxRecords": 5000,
    "format_output": "JSON",
    "aggregateBy": None,
    "breakdownMode": "classic",
    "countOnly": None,
    "includeDesc": True
}

data = comtradeapicall.getFinalData(
    subscription_key=sub_key, **selection_criteria, **query_options
)

print(data.iloc[0].keys())
# print(data.iloc[0])
# print(data.iloc[1])
# print(data.iloc[2])


# selection_criteria = {
#     'typeCode': 'C',  # Goods
#     'freqCode': 'M',  # Monthly
#     'clCode': 'HS',  # Harmonized System
#     'reporterCode': '643',  # Russia
#     'cmdCode': '04',  # HS code for milk
#     'flowCode': None,  # Export
#     'partnerCode': None,  # All partner countries
#     'partner2Code': None,
#     'customsCode': None,
#     'motCode': None
# }
#
# # Define the query options
# query_options = {
#     'maxRecords': 50000,  # Maximum number of records to return
#     'format_output': 'JSON',  # Output format
#     'aggregateBy': None,
#     'breakdownMode': 'classic',
#     'countOnly': None,
#     'includeDesc': True  # Include descriptions
# }
#
# # Initialize a variable to store the total volume
# total_volume = 0
#
# # Get the data for each quarter of 2017
# for quarter in range(1, 5):
#     # Get the data for each month in the quarter
#     for month in range(1 + (quarter - 1) * 3, 1 + quarter * 3):
#         # Format the month to have two digits
#         month_str = str(month).zfill(2)
#
#         # Set the period to the year and month
#         selection_criteria['period'] = '2017' + month_str
#
#         # Get the data
#         data = comtradeapicall.getFinalData(sub_key,
#                                             **selection_criteria,
#                                             **query_options)
#
#         # Add the volume to the total volume
#         total_volume += data['qty'].sum()
#
# # Print the total volume
# print("Total Volume:", total_volume)
