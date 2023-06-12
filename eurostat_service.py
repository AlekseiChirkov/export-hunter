from datetime import datetime

import eurostat
from dateutil.relativedelta import relativedelta

toc = eurostat.get_toc()

for dataset in toc:
    if 'trade' in dataset[0].lower():
        print(dataset[5], dataset[6])
        # print(dataset)
        # start_date = dataset[5]
        # end_date = dataset[6]
        #
        # start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S%z')
        # end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S%z')
        #
        # delta = relativedelta(end_date, start_date)
        #
        # months = delta.years * 12 + delta.months

        # print(months)



# data = eurostat.get_data_df('DS-059292')
# filtered_data = tuple(row for row in data if row['CN code'] == '010229')
# print(filtered_data)
