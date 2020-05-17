
def active_summary(data):
    data['Active'] = data['Cases']
    return data.loc[:,['Active']]
