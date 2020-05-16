import io

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from flask import Flask, render_template, Response

import covid19india as ind

app = Flask(__name__)

state_wise_summary = "https://api.covid19india.org/csv/latest/state_wise.csv"
case_time_series = "https://api.covid19india.org/csv/latest/case_time_series.csv"
korea_summary = "https://api.apify.com/v2/datasets/Lc0Hoa8MgAbscJA4w/items?format=csv&clean=1"

def load_csv_data(uri):
    data = pd.read_csv(uri)
    return data

def chartImage(ax):
    output = io.BytesIO()
    FigureCanvas(ax.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/death.png')
def death_rate():
    data = load_csv_data(state_wise_summary)
    death_rate = ind.state_wise_death_ratio(data)
    death_rate = death_rate.set_index('State')

    ax = death_rate.plot(figsize=(10,7), kind='bar')
    ax.set_ylabel('Percentage')
    return chartImage(ax)

@app.route('/new.png')
def new_cases():
    data = load_csv_data(case_time_series)
    data = data.tail(46)
    data = data.head(45)
    growth_rates = ind.new_and_recovered(data)
    growth_rates = growth_rates.set_index('Date')

    ax = growth_rates.plot(figsize=(10,5))
    return chartImage(ax)

@app.route('/growth.png')
def growth_rate():
    data = load_csv_data(case_time_series)
    data = data.tail(46)
    data = data.head(45)
    growth_rates = ind.cases_growth_chart(data)
    growth_rates = growth_rates.set_index('Date')

    ax = growth_rates.plot(figsize=(10,5), grid=True)
    ax.set_ylabel('Growth Rate')
    return chartImage(ax)

@app.route('/total.png')
def total():
    data = load_csv_data(case_time_series)
    data = data.tail(46)
    data = data.head(45)
    growth_rates = ind.cases_total_chart(data)
    growth_rates = growth_rates.set_index('Date')

    ax = growth_rates.plot(figsize=(10,5), grid=True)
    return chartImage(ax)

@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template('home.htm')
