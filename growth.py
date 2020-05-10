
import random as r
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

case_time_series = "https://api.covid19india.org/csv/latest/case_time_series.csv"

def load_csv_data(uri):
    data = pd.read_csv(uri)
    return data

def cases_growth_chart(data):
    data['Total Active'] = data['Total Confirmed'] - data['Total Recovered'] - data['Total Deceased']
    data['GR (C)'] = data['Total Confirmed'].pct_change()
    data['GR (A)'] = data['Total Active'].pct_change()

    data['5-day GR (C)'] = data['GR (C)'].rolling(5).mean()
    data['5-day GR (A)'] = data['GR (A)'].rolling(5).mean()
    #lines = data.plot.line()
    return data.loc[:,['Date','Total Confirmed','Total Active','GR (C)','GR (A)','5-day GR (C)','5-day GR (A)']]

def line_chart(df, idx):
    df = df.set_index(idx)
    df.plot(figsize=(10,5), grid=True)
    plt.show()

def line_chart_secondary(df, idx):
    df = df.set_index(idx)
    ax = df.plot(secondary_y=['5-day GR (C)','5-day GR (A)'], grid=True)
    ax.set_ylabel('Total Cases')
    ax.right_ax.set_ylabel('Growth Rate Moving Avg')
    plt.show()

# Cases Growth Rates
data = load_csv_data(case_time_series)
data = data.tail(45)
growth_rates = cases_growth_chart(data)
#print(growth_rates)

line_chart_secondary(growth_rates, 'Date')
