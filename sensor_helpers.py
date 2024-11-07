import pandas as pd
from pandas.tseries.frequencies import to_offset


def get_frequency(idx):
    """Get the frequency string for a datetime index"""
    diffs = idx[1:] - idx[:-1]
    offset = to_offset(diffs.min())
    
    return offset.freqstr
    

def initialize_range(df, percent=10, period=None):
    # determine num periods to make the range slider based on percent of series length or a specified timedelta
    r, c = df.shape
    if period:
        samples = int(period/pd.to_timedelta(df.index.freq))
        range_width = min([samples, r-1])
    else:
        range_width = int(r*percent/100)
        
    return range_width
        
        
def load_df(srcdir, file):
    df = pd.read_parquet(srcdir + '/' + file)

    # update the frequency
    if df.index.freq is None:
        frequency = get_frequency(df.index)
        print(f'index frequency is None, updating to {frequency}')
        df = df.asfreq(frequency)

    return df