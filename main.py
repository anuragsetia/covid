import io

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from flask import Flask, render_template, Response, request

import covid19india as ind
import covid19api as world

app = Flask(__name__)

#covid19india endpoints
state_wise_summary = "https://api.covid19india.org/csv/latest/state_wise.csv"
state_wise_time_series = "https://api.covid19india.org/csv/latest/state_wise_daily.csv"
case_time_series = "https://api.covid19india.org/csv/latest/case_time_series.csv"

#covid19api endpoints
country_summary = "https://api.covid19api.com/total/country/{}/status/confirmed"

#apify endpoints
#korea_summary = "https://api.apify.com/v2/datasets/Lc0Hoa8MgAbscJA4w/items?format=csv&clean=1"
#spain_summary = "https://api.apify.com/v2/datasets/hxwow9BB75z8RV3JT/items?format=csv&clean=1"

#endpoint for totals
india_summary = "https://coronavirus-19-api.herokuapp.com/countries/india"


def load_csv_data(uri):
    data = pd.read_csv(uri)
#    print(data.dtypes)
    return data

def load_json_Data(uri):
    data = pd.read_json(uri)
    return data

def chartImage(ax):
    output = io.BytesIO()
    FigureCanvas(ax.figure).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

# compare confirmed case curve with other countries
@app.route('/compare-active.png')
def vs_country():
    comp_nt_phrase = request.args.get('country')
    comp_nt = load_json_Data(country_summary.format(comp_nt_phrase))
    comp_nt = world.active_summary(comp_nt)
    comp_nt = comp_nt[comp_nt['Active'] >= 1000].reset_index()
    comp_nt[comp_nt_phrase] = comp_nt['Active']
    comp_nt = comp_nt.loc[:,[comp_nt_phrase]]

    india = load_csv_data(case_time_series)
    compared = ind.cases_total_chart(india)
    compared['India'] = compared['Total Confirmed']
    compared = compared[compared['India'] >=1000].reset_index()
    compared = compared.loc[:,['India']]
#    compared['Active (KOR)'] = comp_nt['Active'].to_numpy()
    compared = pd.concat([compared, comp_nt], axis=1)

    ax = compared.plot(figsize=(10,5))
    ax.set_xlabel('Days from 1000 cases')
    return chartImage(ax)

@app.route('/death.png')
def death_rate():
    data = load_csv_data(state_wise_summary)
    death_rate = ind.state_wise_death_ratio(data)
    death_rate = death_rate.set_index('State')

    ax = death_rate.plot(figsize=(10,7), kind='bar')
    ax.set_ylabel('Percentage')
    return chartImage(ax)

@app.route('/state-top.png')
def state_top():
    data = load_csv_data(state_wise_time_series)
    top_states = ind.top_growing_states(data)

    ax = top_states.plot(figsize=(10,7), kind='bar')
    ax.set_ylabel('Avg. New Cases / day')
    return chartImage(ax)

@app.route('/new.png')
def new_cases():
    data = load_csv_data(case_time_series)
    data = data.tail(45)
    growth_rates = ind.new_and_recovered(data)
    growth_rates = growth_rates.set_index('Date')

    ax = growth_rates.plot(figsize=(10,5))
    return chartImage(ax)

@app.route('/growth.png')
def growth_rate():
    data = load_csv_data(case_time_series)
    data = data.tail(45)
    #data = data.head(45)
    growth_rates = ind.cases_growth_chart(data)
    growth_rates = growth_rates.set_index('Date')

    ax = growth_rates.plot(figsize=(10,5), grid=True)
    ax.set_ylabel('Growth Rate')
    return chartImage(ax)

@app.route('/total.png')
def total():
    data = load_csv_data(case_time_series)
    data = data.tail(45)
    growth_rates = ind.cases_total_chart(data)
    growth_rates = growth_rates.set_index('Date')

    ax = growth_rates.plot(figsize=(10,5), grid=True)
    return chartImage(ax)

@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template('home.htm')
