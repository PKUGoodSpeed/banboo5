"""Feature classes."""


class SlidingWindowFeatures(object):
    """Builds sliding window features.

    Usage:
        swf = SlidingWindowFeatures(df)
        df = swf.add_sliding_window_feature(
            'Open', window_size=5, aggr_type='mean').add_sliding_window_feature(
            ...)...build()
    """
    
    def __init__(self, df):
        self._data = df

    def add_sliding_window_feature(self, col, window_size, aggr_type):
        """Adds a sliding window feature to the data.
        
        Args:
            col: The string name of the column to be aggregated.
            window_size: The integer size of the sliding window.
            aggr_type: One of ['max', 'min', 'mean', 'median'].
        """
        assert col in self._data.columns, f'missing column {col}'
        assert aggr_type in ['max', 'min', 'mean', 'median'], f'invalid aggregation type: {aggr_type}'
        feature_name = f'{col}_{window_size}d_{aggr_type}'
        self._data[feature_name] = self._data[col].rolling(
            window_size, min_periods=1).agg(aggr_type)
        return self
    
    def build(self):
        return self._data
    
    def get_data(self):
        return self._data


if __name__ == '__main__':
    import pandas as pd
    df = pd.DataFrame({
        'Open': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'Close': [2, 4, 6, 8, 10, 1, 1, 1, 1, 1]
    })
    df = SlidingWindowFeatures(df).add_sliding_window_feature(
        col='Open', window_size=5, aggr_type='max').add_sliding_window_feature(
        col='Open', window_size=5, aggr_type='min').add_sliding_window_feature(
        col='Open', window_size=3, aggr_type='mean').add_sliding_window_feature(
        col='Open', window_size=3, aggr_type='median').add_sliding_window_feature(
        col='Close', window_size=2, aggr_type='mean').build()
    print(df)
