from datetime import datetime as dt
import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import pytz
 
style.use('seaborn-paper')
pd.set_option('display.max_rows', 10) 
pd.set_option('display.width', None)      
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Currency:
    def __init__(self, currency_type, date_from, date_to, time_frame):

        self.currency_type = currency_type
        self.date_from = date_from
        self.date_to = date_to
        self.time_frame = time_frame

    def get_data(self):
        mt5.initialize()
        # set time zone to UTC
        timezone = pytz.timezone("Etc/UTC")       
        # create 'datetime' objects in UTC time zone to avoid the implementation of a local time zone offset
        utc_from = dt(self.date_from.year, self.date_from.month, self.date_from.day, 00, 00, tzinfo=timezone)
        utc_to = dt(self.date_to.year, self.date_to.month, self.date_to.day, 23, 59, tzinfo=timezone)

        if self.time_frame == 0:
            data_values = mt5.copy_ticks_range(self.currency_type, utc_from, utc_to, mt5.COPY_TICKS_ALL)
        else:
            data_values = mt5.copy_rates_range(self.currency_type, self.time_frame, utc_from, utc_to)

        print(self.currency_type ," Data Points received: ", len(data_values))
        # shut down connection to the MetaTrader 5 terminal
        mt5.shutdown()
        data_frame = pd.DataFrame(data_values)
        # print(ticks_frame)
        return data_frame
     
    def check_currency(self):
        currencies = ["NZDJPY","AUDJPY","USDJPY","CHFJPY","GBPJPY","EURJPY","CADJPY"]
        if self.currency_type in currencies: 
            multi_value = 100
        else:
            multi_value = 10000 

        return multi_value


    def cal_bid_ask_different(self):
        data_frame = self.get_data()

        if data_frame is not None: 
            multi_value = self.check_currency()

            data_frame['ask_bid_change'] = (data_frame['ask'] - data_frame['bid'])*multi_value
            data_frame = data_frame[['time', 'bid', 'ask', 'ask_bid_change']]
            # convert time in seconds into the datetime format
            data_frame['time']=pd.to_datetime(data_frame['time'], unit='s')
            data_frame.fillna(0 , inplace = True)
            # print(data_frame)
     
            return data_frame

        else:
            print("Data receiving problem...")


    def cal_price_present_change(self):
        data_frame = self.get_data()

        if data_frame is not None:           
            data_frame = data_frame[['time', 'open', 'high', 'low', 'close', 'tick_volume']]
            # convert time in seconds into the datetime format
            data_frame['time']=pd.to_datetime(data_frame['time'], unit='s')
            data_frame.fillna(0 , inplace = True)
            data_frame['close_present_change'] = data_frame.close.pct_change() * 100    #precentage change 
            # print(data_frame)

            return data_frame

        else:
            print("Data receiving problem...")

    




#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def draw_chart(data_frame):

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # ax.spines['left'].set_position(('data', 0.0))
    ax.spines['bottom'].set_position(('data', 0.0))
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    plt.plot(data_frame['time'], data_frame.iloc[:,-1],  label = currency_type, linewidth=1)
    for label in ax.xaxis.get_ticklabels():
        label.set_rotation(45)
    plt.legend()
    plt.show()    




currency_type = "USDJPY"
date_from = dt(2020, 5,11)
date_to = dt(2020, 6, 11)
time_frame = mt5.TIMEFRAME_H4

instance = Currency(currency_type, date_from, date_to, time_frame)
# data_frame = instance.cal_bid_ask_different()
# draw_chart(data_frame)

data_frame = instance.cal_price_present_change()
draw_chart(data_frame)



