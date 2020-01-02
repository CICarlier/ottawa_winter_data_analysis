#import useful libraries for data manipulation
import pandas as pd
import numpy as np

#import all daily and hourly files
daily_2013 = pd.read_csv("Ottawa winter weather data/data/en_climate_daily_ON_6105976_2013_P1D.csv")
daily_2014 = pd.read_csv("Ottawa winter weather data/data/en_climate_daily_ON_6105976_2014_P1D.csv")
daily_2015 = pd.read_csv("Ottawa winter weather data/data/en_climate_daily_ON_6105976_2015_P1D.csv")
daily_2016 = pd.read_csv("Ottawa winter weather data/data/en_climate_daily_ON_6105976_2016_P1D.csv")
daily_2017 = pd.read_csv("Ottawa winter weather data/data/en_climate_daily_ON_6105976_2017_P1D.csv")
daily_2018 = pd.read_csv("Ottawa winter weather data/data/en_climate_daily_ON_6105976_2018_P1D.csv")
daily_2019 = pd.read_csv("Ottawa winter weather data/data/en_climate_daily_ON_6105976_2019_P1D.csv")

hourly_2013 = pd.read_csv('Ottawa winter weather data/data/hourly_data_2013.csv')
hourly_2014 = pd.read_csv('Ottawa winter weather data/data/hourly_data_2014.csv')
hourly_2015 = pd.read_csv('Ottawa winter weather data/data/hourly_data_2015.csv')
hourly_2016 = pd.read_csv('Ottawa winter weather data/data/hourly_data_2016.csv')
hourly_2017 = pd.read_csv('Ottawa winter weather data/data/hourly_data_2017.csv')
hourly_2018 = pd.read_csv('Ottawa winter weather data/data/hourly_data_2018.csv')
hourly_2019 = pd.read_csv('Ottawa winter weather data/data/hourly_data_2019.csv')


# To compare winters, we first need to combine the months of October, November, December of one year
# with the months of January, February, March and April of the following year.
# We cannot include winter 2019-2020 yet since it just started.

def winter(x, y):
    oct_nov_dec = x[x.Month.isin([10, 11, 12])]
    jan_feb_mar_apr = y[y.Month.isin([1, 2, 3, 4])]
    winter = pd.concat([oct_nov_dec, jan_feb_mar_apr])
    return winter


daily_2013_2014 = winter(daily_2013, daily_2014)
daily_2013_2014.name = "2013-2014"
daily_2014_2015 = winter(daily_2014, daily_2015)
daily_2014_2015.name = "2014-2015"
daily_2015_2016 = winter(daily_2015, daily_2016)
daily_2015_2016.name = "2015-2016"
daily_2016_2017 = winter(daily_2016, daily_2017)
daily_2016_2017.name = "2016-2017"
daily_2017_2018 = winter(daily_2017, daily_2018)
daily_2017_2018.name = "2017-2018"
daily_2018_2019 = winter(daily_2018, daily_2019)
daily_2018_2019.name = "2018-2019"

hourly_2013_2014 = winter(hourly_2013, hourly_2014)
hourly_2013_2014.name = "2013-2014"
hourly_2014_2015 = winter(hourly_2014, hourly_2015)
hourly_2014_2015.name = "2014-2015"
hourly_2015_2016 = winter(hourly_2015, hourly_2016)
hourly_2015_2016.name = "2015-2016"
hourly_2016_2017 = winter(hourly_2016, hourly_2017)
hourly_2016_2017.name = "2016-2017"
hourly_2017_2018 = winter(hourly_2017, hourly_2018)
hourly_2017_2018.name = "2017-2018"
hourly_2018_2019 = winter(hourly_2018, hourly_2019)
hourly_2018_2019.name = "2018-2019"

daily_datasets = [daily_2013_2014, daily_2014_2015, daily_2015_2016,
                  daily_2016_2017, daily_2017_2018, daily_2018_2019]
hourly_datasets = [hourly_2013_2014, hourly_2014_2015, hourly_2015_2016,
                   hourly_2016_2017, hourly_2017_2018, hourly_2018_2019]


#Now let's aggregate all hourly dataframes into one
def make_hourly_dataset(df):

    #Create dataframe with first, last, min and max temperature for each day
    winter = df.groupby(['Year', "Month", "Day"]).agg({"Temp (°C)": ['first', 'last', "min", "max", "mean"]})
    winter.columns = winter.columns.droplevel()
    winter = winter.reset_index()
    winter['date'] = winter[winter.columns[:3]].apply(lambda x: '-'.join(x.dropna().astype(str)),axis=1)
    winter['date'] = pd.to_datetime(winter['date'])
    #winter['m_d'] = winter[winter.columns[1:3]].apply(lambda x: '-'.join(x.dropna().astype(str)),axis=1)
    winter['winter'] = df.name
    return winter

hourly_all_winters = pd.DataFrame(columns=['Year', "Month", "Day", 'date','first', 'last', "min", "max", "mean"])
for dataset in hourly_datasets:
    df1 = make_hourly_dataset(dataset)
    hourly_all_winters = hourly_all_winters.merge(df1, how='outer')


#And let's do the same with the daily dataframes
for dataset in daily_datasets:
    dataset['winter'] = dataset.name
    dataset['Date/Time'] = pd.to_datetime(dataset['Date/Time'])
cols = [x for x in daily_2013_2014.columns if not x.endswith('Flag')]
daily_all_winters = pd.DataFrame(columns=cols)
for dataset in daily_datasets:
    daily_all_winters = daily_all_winters.merge(dataset[cols], how='outer')
daily_all_winters['Total Snow (cm)']

def get_daily():
    return daily_all_winters


#Result is the hourly_all_winters and the daily_all_winters datasets
