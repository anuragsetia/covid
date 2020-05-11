
import random as r
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

state_wise_summary = "https://api.covid19india.org/csv/latest/state_wise.csv"

def load_csv_data(uri):
    data = pd.read_csv(uri)
    return data

def state_wise_death_ratio(df):
    df['Deaths per Recovered'] = df['Deaths']*100/df['Recovered']
    df['Deaths per Recovered'] = df['Deaths per Recovered'].round(2)
    return df.loc[:,['State','Deaths per Recovered']]

def bar_chart(df, idx):
    df = df.set_index(idx)
    df.plot(figsize=(10,5), kind='bar', grid=True)
    plt.show()

# Death Rate state wise
data = load_csv_data(state_wise_summary)
#print_data_structure(data)
death_rate = state_wise_death_ratio(data)
bar_chart(death_rate, 'State')
