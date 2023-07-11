import squarify
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter


def money_formatter(value: int | float, pos: int) -> str:
    """
    Formatter function to add 'M' or 'B' to y-axis labels for money values
    @param value: money value can be int or float
    @type value: int | float
    @param pos: indicates position of the tick label within the tick locations
    @type pos: int
    @return: formatted value with 'M' or 'B' suffix
    @rtype: str
    """

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f} B"
    else:
        return f"{value / 1_000_000:.1f} M"


def volume_formatter(value: int | float, pos: int) -> str:
    """
    Formatter function to add 'K' to y-axis labels for volume values
    @param value: money value can be int or float
    @type value: int | float
    @param pos: indicates position of the tick label within the tick locations
    @type pos: int
    @return: formatted value with mln suffix
    @rtype: str
    """

    return f"{value / 100000:.1f} K"


def generate_column_chart(chart_name: str, y_label: str, x_label: str,
                          x_axis_labels: list | tuple,
                          values: list | tuple) -> plt:
    """
    Function generates column chart with provided data
    @param chart_name: name of the chart to generate
    @type chart_name: str
    @param y_label: name of values type (USD, Volume, etc.)
    @type y_label: str
    @param x_label: name of x-axis
    @type x_label: str
    @param x_axis_labels: array of labels that will display on x-axis
    @type x_axis_labels: list | tuple
    @param values: array with y-axis values
    @type values: list | tuple
    @return: generated plot
    @rtype: plt
    """

    values = [int(value) for value in values]

    plt.figure(figsize=(16, 6))
    plt.bar(x_axis_labels, values)
    plt.grid(True, alpha=0.25)
    plt.xticks(rotation="vertical")
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.title(chart_name)
    plt.subplots_adjust(top=0.9, bottom=0.15)
    if y_label == "USD":
        plt.gca().yaxis.set_major_formatter(FuncFormatter(money_formatter))
    else:
        plt.gca().yaxis.set_major_formatter(FuncFormatter(volume_formatter))

    return plt


def generate_stacked_area_chart(chart_name: str, x_label: str, y_label: str,
                                data: list[list],
                                countries: list | tuple,
                                periods: list | tuple) -> plt:
    """
    Function generates stacked area chart with provided data
    @param chart_name: name of the chart to generate
    @type chart_name: str
    @param x_label: name of x-axis
    @type x_label: str
    @param y_label: name of y-axis
    @type y_label: str
    @param data: array with arrays inside, each array is data for parameter
    @type data: list
    @param countries: countries with their values to use in y-axis
    @type countries: list | tuple
    @param periods: array of periods to use in x-axis
    @type periods: list | tuple
    @return: generated plot
    @rtype: plt
    """

    plt.stackplot(periods, *data, labels=countries)
    plt.grid(True)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(chart_name)
    plt.legend(loc="upper left")
    return plt


def generate_area_chart(chart_name: str, x_label: str, y_label: str,
                        countries: dict[list | tuple],
                        periods: list | tuple) -> plt:
    """
    Function generates area chart with provided data
    @param chart_name: name of the chart to generate
    @type chart_name: str
    @param x_label: name of x-axis
    @type x_label: str
    @param y_label: name of y-axis
    @type y_label: str
    @param countries: countries with their values to use in y-axis
    @type countries: dict[list | tuple]
    @param periods: array of periods to use in x-axis
    @type periods: list | tuple
    @return: generated plot
    @rtype: plt
    """

    for country, values in countries.items():
        plt.plot(periods, values, label=country)

    plt.grid(True)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(chart_name)
    plt.legend()
    return plt


def generate_bubble_chart(chart_name: str, x_label: str, y_label: str,
                          countries: list | tuple,
                          weight: list | tuple,
                          usd: list | tuple) -> plt:
    """
    Function generates bubble chart with provided data
    @param chart_name: name of the chart to generate
    @type chart_name: str
    @param x_label: name of x-axis
    @type x_label: str
    @param y_label: name of y-axis
    @type y_label: str
    @param countries: array of countries to use in chart
    @type countries: list | tuple
    @param weight: array of weight values to use in chart
    @type weight: list | tuple
    @param usd: array of usd values to use in chart
    @type usd: list | tuple
    @return: generated plot
    @rtype: plt
    """

    plt.scatter(usd, weight, s=weight, c=usd, alpha=0.5)
    for index, country in enumerate(countries):
        plt.annotate(country, (usd[index], weight[index]))

    plt.grid(True)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(chart_name)
    return plt


def generate_negative_bar_chart(chart_name: str, x_label: str, y_label: str,
                                amounts: list | tuple,
                                periods: list | tuple) -> plt:
    """
    Function generates bar chart with provided data that shows both
    negative and positive
    @param chart_name: name of the chart to generate
    @type chart_name: str
    @param x_label: name of x-axis
    @type x_label: str
    @param y_label: name of y-axis
    @type y_label: str
    @param amounts: values to draw on chart
    @type amounts: list | tuple
    @param periods: periods (years, months) to draw on chart
    @type periods: list | tuple
    @return: generated plot
    @rtype: plt
    """

    colors = ['green' if amount >= 0 else 'red' for amount in amounts]

    plt.bar(periods, amounts, color=colors)
    plt.grid(True)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(chart_name)
    return plt


def generate_tree_map(chart_name: str, countries: list | tuple,
                      sizes: list | tuple) -> plt:
    """
    Function generated tree map chart with provided data
    @param chart_name: name of the chart to generate
    @type chart_name: str
    @param countries: array of countries to draw square
    @type countries: list | tuple
    @param sizes: array of sizes for each country
    @type sizes: list | tuple
    @return: generated plot
    @rtype: plt
    """

    squarify.plot(
        sizes=sizes, label=countries, color='#9999', edgecolor='#ffff'
    )

    plt.axis('off')
    plt.title(chart_name)
    plt.show()
    return plt


def get_data_for_specified_period_by_month(values: list | tuple,
                                           period: int) -> list:
    return values[:period]


def get_data_for_specified_period_by_year(values: list | tuple,
                                          period: int) -> list:
    counted_month = 0
    yearly_summ = 0
    year_data = []
    for month_data in values:
        counted_month += 1
        yearly_summ += int(month_data)
        if counted_month % 12 == 0:
            year_data.append(yearly_summ)
            yearly_summ = 0

        if counted_month == period:
            break

    return year_data


def get_date_labels_for_year(dates: list | tuple,
                             period: int) -> list:
    year_label = ''
    year_labels = []
    counted_month = 0
    for date in dates:
        year = date[:4]
        counted_month += 1
        if year != year_label:
            year_labels.append(year)
            year_label = year

        if counted_month == period:
            break

    return year_labels


dates = "201801	201802	201803	201804	201805	201806	201807	201808	201809	201810	201811	201812	201901	201902	201903	201904	201905	201906	201907	201908	201909	201910	201911	201912	202001	202002	202003	202004	202005	202006	202007	202008	202009	202010	202011	202012	202101	202102	202103	202104	202105	202106	202107	202108	202109	202110	202111	202112	202201	202202	202203	202204	202205	202206	202207	202208	202209	202210	202211	202212"
volumes = "444337075	360426348	389424148	360147233	1008167108	408294058	424519008	369032296	417212109	395692559	408987174	355386545	424688545	310639758	410317098	322283827	365659162	455042359	345684410	359959275	602485038	374631772	376807516	309702116	306808640	256650351	298224873	274427510	251477444	264023184	537368148	368057098	449898075	345282935	440754076	298420382	356208683	407918850	613616964	353109065	380148931	411555377	340008962	354561412	352109123	300741215	377945854	855216322	420619902	418205778	505268754	432104612	453218540	398443863	420115341	473655219	442318309	489781334	541942751	408134038"
values = "1670797407	1509318504	1656567191	1599759666	1667883302	1608471179	1641067591	1607657581	1579829508	1677292408	1641143712	1414238042	1646551828	1467937914	1539510214	1536787641	1626971832	1459901025	1588720300	1453676750	1462539688	1513002736	1438407135	1299982173	1405441926	1271528779	1313832280	1024727057	1018745557	1103269736	1206478357	1150084223	1329473160	1375904926	1370706984	1367721146	1352050796	1350639436	1606674348	1500269822	1511695537	1552619987	1521043012	1465135309	1556267189	1512575676	1610749628	1562748608	1618980605	1591037024	1849395703	1628114688	1756151726	1716417452	1620314952	1692358941	1760654539	1692976101	1697672064	1475141725"

dates_arr = dates.replace('\t', ' ').split(" ")
volumes_arr = volumes.replace('\t', ' ').split(" ")
values_arr = values.replace('\t', ' ').split(" ")

# one_year_dates = get_data_for_specified_period_by_month(dates_arr, 24)
# one_year_volumes = get_data_for_specified_period_by_month(volumes_arr, 24)
# one_year_values = get_data_for_specified_period_by_month(values_arr, 24)

yearly_volume = get_data_for_specified_period_by_year(volumes_arr, 60)
yearly_value = get_data_for_specified_period_by_year(values_arr, 60)
dates = get_date_labels_for_year(dates_arr, 60)
print(dates)
print(yearly_value)

# yearly_value = get_data_for_specified_period_by_year(volumes_arr, 24)
# dates = get_date_labels_for_year(dates_arr, 24)
# print(dates)
# print(yearly_value)
#
# yearly_value = get_data_for_specified_period_by_year(volumes_arr, 60)
# dates = get_date_labels_for_year(dates_arr, 60)
# print(dates)
# print(yearly_value)

# dates_labels = [f"{date.split(' ')[1]}.{date.split(' ')[0]}" for date in dates]
chart = generate_column_chart('World', "Volume", "Period", dates, yearly_volume)
chart.show()
chart = generate_column_chart('World', "USD", "Period", dates, yearly_value)
chart.show()

# dates = [f"{date[:4]} {date[4:]}" for date in dates_arr]
# months = {
#     "01": "January",
#     "02": "February",
#     "03": "March",
#     "04": "April",
#     "05": "May",
#     "06": "June",
#     "07": "July",
#     "08": "August",
#     "09": "September",
#     "10": "October",
#     "11": "November",
#     "12": "December",
# }


