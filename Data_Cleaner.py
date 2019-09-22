import pandas as pd
import re 
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
np.random.seed(12345)


notclean = pd.read_csv('cleanprep.csv', delimiter=',', error_bad_lines=False,engine = 'python',header = None)

notclean.columns = ['dt', 'name','text','polarity','sensitivity']
notclean = notclean.drop(['name','text'], axis=1)

notclean['dt'] = pd.to_datetime(notclean['dt'])
notclean['DateTime'] = notclean['dt'].dt.floor('h')

vdf = notclean.groupby(pd.Grouper(key='dt',freq='H')).size().reset_index(name='tweet_vol')
vdf.index = pd.to_datetime(vdf.index)
vdf=vdf.set_index('dt')

notclean.index = pd.to_datetime(notclean.index)

vdf['tweet_vol'] =vdf['tweet_vol'].astype(float)

df = notclean.groupby('DateTime').agg(lambda x: x.mean())
df['Tweet_vol'] = vdf['tweet_vol']
df = df.drop(df.index[0])

btcDF = pd.read_csv('btcprice.csv', error_bad_lines=False,engine = 'python')
btcDF['Timestamp'] = pd.to_datetime(btcDF['Timestamp'])
btcDF = btcDF.set_index(pd.DatetimeIndex(btcDF['Timestamp']))
btcDF = btcDF.drop(['Timestamp'], axis=1)
btcDF = btcDF.drop(['Weighted Price'],axis=1 )

Final_df = pd.merge(df,btcDF, how='inner',left_index=True, right_index=True)
Final_df.columns = ['Polarity', 'Sensitivity','Tweet_vol','Open','High','Low', 'Close_Price', 'Volume_BTC', 'Volume_Dollar']
