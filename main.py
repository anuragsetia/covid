import io

from flask import Flask, render_template, Response

import pandas as pd
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

app = Flask(__name__)

state_wise_summary = "https://api.covid19india.org/csv/latest/state_wise.csv"
case_time_series = "https://api.covid19india.org/csv/latest/case_time_series.csv"

def load_csv_data(uri):
    data = pd.read_csv(uri)
    return data

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
    data['GR (C)'] = data['Total Confirmed'].pct_change()
    data['GR (A)'] = data['Total Active'].pct_change()

    return data.loc[:,['Date','Total Confirmed','Total Active']]

def chartImage(ax):
    output = io.BytesIO()
    FigureCanvas(ax.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/death.png')
def death_rate():
    data = load_csv_data(state_wise_summary)
    death_rate = state_wise_death_ratio(data)
    death_rate = death_rate.set_index('State')

    ax = death_rate.plot(figsize=(10,7), kind='bar')
    ax.set_ylabel('Percentage')
    return chartImage(ax)

@app.route('/new.png')
def new_cases():
    data = load_csv_data(case_time_series)
    data = data.tail(45)
    growth_rates = new_and_recovered(data)
    growth_rates = growth_rates.set_index('Date')

    ax = growth_rates.plot(figsize=(10,5))
    return chartImage(ax)

@app.route('/growth.png')
def growth_rate():
    data = load_csv_data(case_time_series)
    data = data.tail(45)
    growth_rates = cases_growth_chart(data)
    growth_rates = growth_rates.set_index('Date')

    ax = growth_rates.plot(figsize=(10,5), grid=True)
    ax.set_ylabel('Growth Rate')
    return chartImage(ax)

@app.route('/total.png')
def total():
    data = load_csv_data(case_time_series)
    data = data.tail(45)
    growth_rates = cases_total_chart(data)
    growth_rates = growth_rates.set_index('Date')

    ax = growth_rates.plot(figsize=(10,5), grid=True)
    return chartImage(ax)

@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template('home.htm')
