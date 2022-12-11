import pandas as pd 
import numpy as np 
import statsmodels.api as sm 
from statsmodels.regression.linear_model import OLS 
import matplotlib.pyplot as plt 

class OBanalysis:
    def ofi(self, original_df:pd.DataFrame)-> pd.DataFrame:
        df = original_df.copy()
        df['mid-price-change'] = ((df['bid'] - df['ask'])/2).diff().div(0.1)
        df['prev-bid'] = df['bid'].shift()
        df['prev-bid-size'] = df['bid-size'].shift()
        df['prev-ask'] = df['ask'].shift()
        df['prev-ask-size'] = df['ask-size'].shift()
        df.dropna(inplace =True)

        bid_geq = df['bid'] >= df['prev-bid']
        bid_leq = df['bid'] <= df['prev-bid']
        ask_geq = df['ask'] >= df['prev-ask']
        ask_leq = df['ask'] <= df['prev-ask']

        df['OFI'] = pd.Series(np.zeros(len(df)))
        df['OFI'].loc[bid_geq] += df['bid-size'].loc[bid_geq]
        df['OFI'].loc[bid_leq] += df['prev-bid-size'].loc[bid_leq]
        df['OFI'].loc[ask_geq] += df['prev-ask-size'].loc[ask_geq]
        df['OFI'].loc[ask_leq] += df['ask-size'].loc[ask_leq]
        return df
    def plot_ofi_and_ols_summary(self, df: pd.DataFrame)->pd.DataFrame:
        df.plot(kind='scatter', grid=True, 
                    x='OFI', y='mid-price-change', 
                    title = 'OFI',
                    alpha=0.5, figsize=(12,10))
        ofi_ = sm.add_constant(df['OFI'])
        ols = OLS(df['mid-price-change'], ofi_).fit()
        print(ols.summary2())

