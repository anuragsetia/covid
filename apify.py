import pandas as pd
import numpy as np

def cases_total_chart(data):
#    data['Date'] = data['lastUpdatedAtSource']
#    data['Total Confirmed'] = data['infected']
    data['Active'] = data['Isolated'].fillna(0.0).astype(int)
    return data.loc[:,['Active']]

def cases_total_spain(data):
    data['Active'] = data['hospitalised'].fillna(0.0).astype(int)
    return data.loc[:,['Active']]
