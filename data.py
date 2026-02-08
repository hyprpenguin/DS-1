import pandas as pd

df=pd.read_csv("time_series_covid19_confirmed_global.csv")

df_reduced=df.drop(['Lat', 'Long'], axis=1)

df_long=df_reduced.melt(id_vars=["Province/State", "Country/Region"],
                var_name='Date',
                value_name='Confirmed')

#print(df_long[df_long["Country/Region"]=='Afghanistan'].head(10))

df_long['Date']=pd.to_datetime(df_long['Date'])

#df_long.info()

df_long['Province/State']=df_long['Province/State'].fillna(df_long['Country/Region'])

#print(df_long.isnull().sum())

df_long['New Cases']=df_long.groupby(['Province/State', 'Country/Region'])['Confirmed'].diff()

#print(df_long[df_long['Country/Region'] == 'India'].tail(10))

df2=pd.read_csv("time_series_covid19_deaths_global.csv")

#print(df2)

df2_reduced=df2.drop(['Lat', 'Long'], axis=1)

#print(df2_reduced)

df2_long=df2_reduced.melt(id_vars=['Province/State', 'Country/Region'],
  var_name='Date',
  value_name='Confirmed Deaths')

print(df2_long)

df2_long['Province/State']=df2_long['Province/State'].fillna(df2_long['Country/Region'])

df2_long['New Deaths']=df2_long.groupby(['Province/State', 'Country/Region'])['Confirmed Deaths'].diff()

#print(df2_long[df2_long['Country/Region'] == 'India'].tail(10))

