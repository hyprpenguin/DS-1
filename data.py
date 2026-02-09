import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

df=pd.read_csv("time_series_covid19_confirmed_global.csv")

df_reduced=df.drop(['Lat', 'Long'], axis=1)

df_long=df_reduced.melt(id_vars=["Province/State", "Country/Region"],
                var_name='Date',
                value_name='Confirmed Cases')

#print(df_long[df_long["Country/Region"]=='Afghanistan'].head(10))

df_long['Date']=pd.to_datetime(df_long['Date'])

#df_long.info()

df_long['Province/State']=df_long['Province/State'].fillna(df_long['Country/Region'])

#print(df_long.isnull().sum())

df_long['New Cases']=df_long.groupby(['Province/State', 'Country/Region'])['Confirmed Cases'].diff()

#print(df_long[df_long['Country/Region'] == 'India'].tail(10))

df2=pd.read_csv("time_series_covid19_deaths_global.csv")

#print(df2)

df2_reduced=df2.drop(['Lat', 'Long'], axis=1)

#print(df2_reduced)

df2_long=df2_reduced.melt(id_vars=['Province/State', 'Country/Region'],
  var_name='Date',
  value_name='Confirmed Deaths')

df2_long['Date']=pd.to_datetime(df2_long['Date'])

#print(df2_long)

df2_long['Province/State']=df2_long['Province/State'].fillna(df2_long['Country/Region'])

df2_long['New Deaths']=df2_long.groupby(['Province/State', 'Country/Region'])['Confirmed Deaths'].diff()

#print(df2_long[df2_long['Country/Region'] == 'India'].tail(10))

df_final=pd.merge(df_long, df2_long, on=['Province/State', 'Country/Region', 'Date'])

#print(df_final[df_final['Country/Region'] == 'India'].tail(10))

df_final['CFR']=np.where(df_final['Confirmed Cases']!=0, (df_final['Confirmed Deaths'] / df_final['Confirmed Cases']) * 100, 0)

#print(df_final[df_final['Country/Region'] == 'India'])

#print(df_final.sort_values(by='CFR', ascending=False).head(10))

country_summary=df_final.groupby('Country/Region').tail(1)

#print(country_summary.sort_values(by='CFR', ascending=False))

mask=country_summary['Confirmed Cases'] > 10000
significant_countries=country_summary[mask]

top_10_plot=significant_countries.sort_values(by='CFR', ascending=False).head(10)


plt.bar(top_10_plot['Country/Region'], top_10_plot['CFR'], color='Brown')

plt.title("Top 10 countries affected most by Covid-19")
plt.xlabel("Country")
plt.ylabel("CFR")
plt.xticks(rotation=45, ha='right')

plt.show()

#CFR=(Confirmed Deaths/Confirmed Cases)*100

#Analysis shows that Yemen, Sudan, and Syria have significantly higher CFRs compared to the global average. 
#This suggests that while case counts might be lower in these regions, 
#the severity of the outcomes for those infected is much higher,
#potentially due to healthcare infrastructure challenges.


