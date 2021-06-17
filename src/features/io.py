import os
import numpy as np
import pandas as pd


class DataReader:
    
    def __init__(self,
                 data_dir,
                 start_date_str,
                 end_date_str,
                 date_col='Date',
                 symbol_list=None,
                 file_suffix='.us.txt'):
        symbol_list = symbol_list or [
            f.split(file_suffix)[0] for f in os.listdir(data_dir)
            if f.endswith(file_suffix)
        ]
        self._paths_by_symbols = dict()
        for s in symbol_list:
            filename = s + file_suffix
            if filename in os.listdir(data_dir):
                self._paths_by_symbols[s] = os.path.join(data_dir, filename)
            else:
                print(f'No data for symbol: {s}.')
        
        self._date_col = date_col
        self._start_date = start_date_str
        self._end_date = end_date_str
        self._weekday_df = pd.DataFrame({
            date_col: pd.bdate_range(start=start_date_str, end=end_date_str).astype(str)
        })
        self._data_by_symbols = dict()
        
    def process_data_for_one_symbol(self, df_symbol):
        df_symbol[self._date_col] = df_symbol[self._date_col].astype(str)
        df_symbol = df_symbol[(df_symbol[self._date_col] >= self._start_date) & (
            df_symbol[self._date_col] <= self._end_date)]
        coverage = 1. * df_symbol.shape[0] / self._weekday_df.shape[0]
        return pd.merge(
            self._weekday_df, df_symbol, on=[self._date_col], how='left').ffill(), coverage
    
    def process_date(self):
        for symbol, filepath in self._paths_by_symbols.items():
            data, coverage = self.process_data_for_one_symbol(pd.read_csv(filepath))
            self._data_by_symbols[symbol] = {
                'data': data,
                'coverage': coverage
            }
        return self._data_by_symbols


if __name__ == '__main__':
    data_reader = DataReader(
        data_dir='../../data/Stocks',
        start_date_str='2017-11-04',
        end_date_str='2017-11-08',
        symbol_list=['iba', 'goog', 'nosymbol']
    )
    data_map = data_reader.process_date()
    for symbol, data in data_map.items():
        print(symbol, data['coverage'])
        print(data['data'])


                
        
        
        
    
        