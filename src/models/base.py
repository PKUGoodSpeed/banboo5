"""ModelBase class."""
import abc


class ModelBase(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def build_model(self, **params):
        raise NotImplementedError
    
    @abc.abstractmethod
    def train_model(self, train_df, valid_df, **params):
        raise NotImplementedError
        
    @abc.abstractmethod
    def evaluate(self, valid_df, **params):
        raise NotImplementedError
    
    @abc.abstractmethod
    def predict(self, test_df, output_col='predict'):
        raise NotImplementedError
    
    @abc.abstractmethod
    def save_model(self, model_path):
        raise NotImplementedError
    
    @abc.abstractmethod
    def load_model(self, model_path):
        raise NotImplementedError


class TestModel(ModelBase):
    
    def build_model(self, k, b):
        self._k = k
        self._b = b
        return self

    def train_model(self, train_df, valid_df, **params):
        self._k = (train_df['x'] * train_df['y']).mean() / (
            train_df['x'] * train_df['x'] + 1.E-10).mean()
        self._b = train_df['y'].mean() - self._k * train_df['x'].mean()
        return self
    
    def evaluate(self, valid_df):
        pred = self._k * valid_df['x'] + self._b
        mse = ((pred - valid_df['y']) * (pred - valid_df['y'])).mean()
        return dict(mse=mse)

    def predict(self, test_df, output_col='predict'):
        test_df[output_col] = self._k * test_df['x'] + self._b
        return test_df

    def save_model(self, model_path):
        return model_path
    
    def load_model(self, model_path):
        return model_path


if __name__ == '__main__':
    import pandas as pd
    tm = TestModel()
    train_df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 6, 7, 8],
        'y': [4, 5, 6, 7, 8, 9, 11, 12]
    })
    pred = tm.build_model(k=0, b=0).train_model(
        train_df, None).predict(test_df=train_df)
    print(pred)
    print(tm.evaluate(train_df))
    