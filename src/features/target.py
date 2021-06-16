r"""Util functions to compose proper training targets.

As of 2021-06-16, we use price movements as a general training target. We will consider two scenarios:
    1. What is the overall moving trend of the price, increasing or decreasing by multi-day average.
    2. Whether there exists a time point (in the short future) at which the limit buy/sell order can be filled.
"""


class PriceMovementTarget:

    def __init__(self, data, verbose=0):
        """The class constructor.
        
        data: The DataFrame contains the raw price time series.
        verbose: Whether to record the intermediate columns.
        """
        self._data = data
        self._verbose = verbose

    def get_price_movement(self,
                           data,
                           price_col,
                           horizon,
                           sliding_aggr_mode='mean',
                           verbose=0):
        """Returns a DataFrame with added columns indicating the price movements.
        
        data: The DataFrame contains the raw price time series.
        price_col: The target price column of interest.
        horizon: The time window length.
        sliding_aggr_mode: One of 'mean', 'max' and 'min'.
        verbose: 0: the movement ratio; 1: the sliding window aggr; 2: next day price.
        """
        next_day_price = data[price_col].shift(-1).astype(float)
        future_xday_agg = data[price_col].rolling(horizon).agg(
            sliding_aggr_mode).shift(-horizon).astype(float)
        price_moving_ratio = future_xday_agg / (next_day_price + 1.E-10)
        data[f'future_{horizon}day_{sliding_aggr_mode}_{price_col}_ratio'] = price_moving_ratio
        if verbose >= 1:
            data[f'future_{horizon}day_{sliding_aggr_mode}_{price_col}'] = future_xday_agg
        if verbose >= 2:
            data[f'next_day_{price_col}'] = next_day_price
        return data
    
    def add_future_high_point(self, high_price_col, horizon):
        self._data = self.get_price_movement(
            self._data, high_price_col, horizon, 'max', self._verbose)
        return self

    def add_future_low_point(self, low_price_col, horizon):
        self._data = self.get_price_movement(
            self._data, low_price_col, horizon, 'min', self._verbose)
        return self
    
    def add_future_avg_point(self, avg_price_col, horizon):
        self._data = self.get_price_movement(
            self._data, avg_price_col, horizon, 'mean', self._verbose)
        return self

    def get_data(self):
        return self._data


if __name__ == '__main__':
    import pandas as pd
    test_df = pd.DataFrame({
        'High': [10, 20, 30, 40, 50, 60, 70, 80, 80, 80],
        'Low': [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    })
    print(test_df)
    df_with_target = PriceMovementTarget(data=test_df, verbose=1).add_future_high_point(
        'High', 3).add_future_low_point('Low', 3).add_future_avg_point('Low', 3).get_data()
    print(df_with_target)
                