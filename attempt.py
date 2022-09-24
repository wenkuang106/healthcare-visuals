##### Importing the Packages #####

from select import select
import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.express as px ## if not code doesn't work remember to use 'pip install plotly' on terminal 

##### Loading in Data ##### 

df = pd.read_csv('https://raw.githubusercontent.com/wenkuang106/AHI_Microcourse_Visualization/main/Data/Georgia_COVID/Georgia_COVID-19_Case_Data.csv')
df
len(df)
df.shape

##### Describing the Variables ##### 

df.info()
list(df)
df['COUNTY'].value_counts()
df_counties = df['COUNTY'].value_counts()
df_counties.head(5)

##### Transforming Columns ##### 

df['DATESTAMP']

## creating a copy of the existing column, so we keep the original version 
## we could also override the column if we wanted to, but because we are unsre 
## where are going to take the analysis - lets just keep it 

df['DATESTAMP_MOD'] = df['DATESTAMP']
print(df['DATESTAMP_MOD'].head(10))
print(df['DATESTAMP_MOD'].dtypes)

df['DATESTAMP_MOD'] = pd.to_datetime(df['DATESTAMP_MOD'])
df['DATESTAMP_MOD'].dtypes

df[['DATESTAMP', 'DATESTAMP_MOD']]
df['DATESTAMP_MOD_DAY'] = df['DATESTAMP_MOD'].dt.date
df['DATESTAMP_MOD_DAY']

df['DATESTAMP_MOD_YEAR'] = df['DATESTAMP_MOD'].dt.year
df['DATESTAMP_MOD_MONTH'] = df['DATESTAMP_MOD'].dt.month
df['DATESTAMP_MOD_YEAR'] 
df['DATESTAMP_MOD_MONTH']

df['DATESTAMP_MOD_MONTH_YEAR'] = df['DATESTAMP_MOD'].dt.to_period('M')
df['DATESTAMP_MOD_MONTH_YEAR'].sort_values()
df

df['DATESTAMP_MOD_WEEK'] = df['DATESTAMP_MOD'].dt.week
df['DATESTAMP_MOD_WEEK']

df['DATESTAMP_MOD_QUARTER'] = df['DATESTAMP_MOD'].dt.to_period('Q')
df['DATESTAMP_MOD_QUARTER'].sort_values()
df['DATESTAMP_MOD_QUARTER']

df['DATESTAMP_MOD_DAY_STRING'] = df['DATESTAMP_MOD_DAY'].astype(str)
df['DATESTAMP_MOD_WEEK_STRING'] = df['DATESTAMP_MOD_WEEK'].astype(str)
df['DATETIME_STRING'] = df['DATESTAMP_MOD_MONTH_YEAR'].astype(str)

##### Gettign the Counties REquired for Our Analysis ##### 

""" 
We know that the counties we want to analyze are: 
- Cobb 
- DeKalb 
- Fulton 
- Gwinnett
- Hall 
"""

df['COUNTY']

countList = ['COBB', 'DEKALB', 'FULTON', 'GWINNETT', 'HALL']
countList

selectCounties = df[df['COUNTY'].isin(countList)]
len(selectCounties)

##### Getting Just the Specific Date/TIME Frame We Want ##### 

""""
`df` = length ~ 90,000
`selectCounties` = length 2,830 
`selectCountyTime` = ???/TBD 
"""
selectCountyTime = selectCounties
selectCountyTime['DATESTAMP_MOD_MONTH_YEAR']

selectCountTime_april2020 = selectCountyTime[selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04']
len(selectCountTime_april2020)
selectCountTime_aprilmay2020 = selectCountyTime[(selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-05') | (selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04')]
len(selectCountTime_aprilmay2020)

selectCountTime_aprilmay2020.head(50)

##### Creating the Final df / Specific Columns-Features-Attributes- that We Care About ##### 

finaldf = selectCountTime_aprilmay2020[[
    'COUNTY' ,
    'DATESTAMP_MOD',
    'DATESTAMP_MOD_DAY',
    'DATESTAMP_MOD_DAY_STRING',
    'DATETIME_STRING', 
    'DATESTAMP_MOD_MONTH_YEAR',
    'C_New', # cases - new
    'C_Cum', # cases - total 
    'H_New', # hospitalizations - new 
    'H_Cum', # hospitalizatiosn - total 
    'D_New', # deaths - new 
    'D_Cum', # deaths - total
]]
finaldf

##### Looking at Total COVID Cases by Month #####

finaldf_dropdups = finaldf.drop_duplicates(subset=['COUNTY','DATETIME_STRING'], keep='last')
finaldf_dropdups

pd.pivot_table(finaldf_dropdups, values='C_Cum', index=['COUNTY'],
columns=['DATESTAMP_MOD_MONTH_YEAR'], aggfunc=np.sum)

vis1 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', data=finaldf_dropdups)
vis2= sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', hue='COUNTY', data=finaldf_dropdups)

plotly1 = px.bar(finaldf_dropdups, x='DATETIME_STRING', y='C_Cum', color='COUNTY', barmode='group')
plotly1.show()

##### Looking at Total COVID Cases by Day ##### 

daily = finaldf 
daily 
len(daily )

pd.pivot_table(daily, values='C_Cum', index=['COUNTY'], columns=['DATESTAMP_MOD_DAY'], aggfunc=np.sum)
tempdf = pd.pivot_table(daily, values='C_Cum', index=['DATESTAMP_MOD_DAY'], columns=['COUNTY'], aggfunc=np.sum)
tempdf.head(50)

startdate = pd.to_datetime("2020-04-26").date()
enddate = pd.to_datetime("2020-05-09").date()

maskFilter = (daily['DATESTAMP_MOD_DAY'] >= startdate) & (daily['DATESTAMP_MOD_DAY'] <= enddate)

dailySpecific = daily.loc[maskFilter]
dailySpecific

dailySpecific[dailySpecific['COUNTY'] == 'FULTON']

vis3 = sns.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum')
vis4 = sns.lineplot(data=dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum', hue='COUNTY')

plotly3 = px.bar(dailySpecific, x='DATESTAMP_MOD_DAY', y='C_Cum', color='COUNTY')
plotly3.show()

plotly4 = px.bar(dailySpecific, 
                x='DATESTAMP_MOD_DAY',
                y='H_New',
                color='COUNTY',
                barmode='group')
plotly4.show()

plotly5 = px.bar(dailySpecific, 
                x='DATESTAMP_MOD_DAY',
                y='H_Cum',
                color='COUNTY',
                barmode='group')
plotly5.show()

plotly6 = px.bar(dailySpecific, 
                x='DATESTAMP_MOD_DAY',
                y='D_New',
                color='COUNTY',
                barmode='group')
plotly6.show()

plotly7 = px.bar(dailySpecific, 
                x='DATESTAMP_MOD_DAY',
                y='D_Cum',
                color='COUNTY',
                barmode='group')
plotly7.show()

dailySpecific['newHosandDeathCovid'] = dailySpecific['D_New'].astype(int) + dailySpecific['H_New'].astype(int) + dailySpecific['C_New'].astype(int)
dailySpecific['newHosandDeathCovid']
dailySpecific

dailySpecific['newHosandDeath'] = dailySpecific['D_New'].astype(int) + dailySpecific['H_New'].astype(int)
dailySpecific['newHosandDeath']

plotly8 = px.bar(dailySpecific, 
                x='DATESTAMP_MOD_DAY',
                y='newHosandDeathCovid',
                color='COUNTY',
                title='Georgia 2020 COVID Data: Total New Hospitalizations , Deaths, and COIVD cases by County',
                labels={
                    "DATESTAMP_MOD_DAY": "Time (Month, Day, Year)",
                    "newHosandDeathCovid": "Total Count"
                },
                barmode='group')
plotly8.update_layout(
    xaxis = dict(
        tickmode = 'linear',
        type='category'
    )
)
plotly8.show()