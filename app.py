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
    df['Deaths per Recovered'] = df['Deaths']*100/df['Recovered']
    df['Deaths per Recovered'] = df['Deaths per Recovered'].round(2)
    return df.loc[:,['State','Deaths per Recovered']]

def cases_growth_chart(data):
    data['Total Active'] = data['Total Confirmed'] - data['Total Recovered'] - data['Total Deceased']
    data['GR (C)'] = data['Total Confirmed'].pct_change()
    data['GR (A)'] = data['Total Active'].pct_change()

    data['5-day GR (C)'] = data['GR (C)'].rolling(5).mean()
    data['5-day GR (A)'] = data['GR (A)'].rolling(5).mean()
    #lines = data.plot.line()
    return data.loc[:,['Date','Total Confirmed','Total Active','GR (C)','GR (A)','5-day GR (C)','5-day GR (A)']]

@app.route('/death.png')
def death_rate():
    data = load_csv_data(state_wise_summary)
    death_rate = state_wise_death_ratio(data)
    death_rate = death_rate.set_index('State')

    ax = death_rate.plot(figsize=(10,5), kind='bar', grid=True)
    output = io.BytesIO()
    FigureCanvas(ax.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/growth.png')
def growth_rate():
    data = load_csv_data(case_time_series)
    data = data.tail(45)
    growth_rates = cases_growth_chart(data)
    growth_rates = growth_rates.set_index('Date')

    ax = growth_rates.plot(figsize=(10,5), secondary_y=['5-day GR (C)','5-day GR (A)'], grid=True)
    ax.set_ylabel('Total Cases')
    ax.right_ax.set_ylabel('Growth Rate Moving Avg')
    output = io.BytesIO()
    FigureCanvas(ax.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template('home.htm')
