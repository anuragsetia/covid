
import pandas as pd
import numpy as np

def state_wise_death_ratio(df):
    df['Death Rate (%age or recovery)'] = df['Deaths']*100/df['Recovered']
    df['Death Rate (%age or recovery)'] = df['Death Rate (%age or recovery)'].round(2)
    return df.loc[:,['State','Death Rate (%age or recovery)']]

def new_and_recovered(df):
    df['New Case Trend'] = df['Daily Confirmed'].rolling(5).mean()
    return df.loc[:,['Date','Daily Confirmed','Daily Recovered', 'New Case Trend']]

def cases_growth_chart(data):
    data['Total Active'] = data['Total Confirmed'] - data['Total Recovered'] - data['Total Deceased']
    data['GR (C)'] = data['Total Confirmed'].pct_change()
    data['GR (A)'] = data['Total Active'].pct_change()

    data['5-day GR (C)'] = data['GR (C)'].rolling(5).mean()
    data['5-day GR (C)'] = data['5-day GR (C)'].round(3)*100
    data['5-day GR (A)'] = data['GR (A)'].rolling(5).mean()
    data['5-day GR (A)'] = data['5-day GR (A)'].round(3)*100
    #lines = data.plot.line()
    return data.loc[:,['Date', '5-day GR (C)','5-day GR (A)']]

def cases_total_chart(data):
    data['Total Active'] = data['Total Confirmed'] - data['Total Recovered'] - data['Total Deceased']
    return data.loc[:,['Date','Total Confirmed','Total Active']]
