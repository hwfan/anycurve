import pandas as pd
import os
import numpy as np
class curvedb(object):
    '''
    database class for storing curve data.
    '''
    def __init__(self, db_path=None, db_name='curvedb'):
        self.db_name = db_name
        self.db_path = db_path
        assert self.db_path is not None
        assert len(self.db_path) > 0
        self.initialize()
        
    def initialize(self):
        try:
            self.load()
        except:
            self.db = pd.DataFrame()
            self.save()

    def reset(self, force_clean=False):
        self.db = pd.DataFrame()
        if force_clean:
            h5_store = pd.HDFStore(self.db_path)
            h5_store.remove(self.db_name)
            h5_store.close()

    def get_db(self):
        return self.db

    @property
    def keys(self):
        return list(self.db.keys())
    
    @property
    def cursor(self):
        return len(self.db)

    def get_column(self, key):
        return self.db[key].to_numpy()

    def add_key(self, key):
        if isinstance(key, list):
            for each_key in key:
                self.db[each_key] = np.nan
        else:
            self.db[key] = np.nan

    def delete_key(self, key):
        if isinstance(key, list):
            self.db.drop(columns=key, inplace=True)
        else:
            self.db.drop(columns=[key], inplace=True)
            
    def search_value(self, key, target_value):
        return self.db[key] == target_value

    def check_index(self, index):
        return index < len(self.db)

    def get_value(self, index):
        return self.db.loc[index]

    def add_value(self, dict_value):
        assert isinstance(dict_value, dict), 'The input of add_value should be a dict variable!'

        for key in dict_value:
            if key not in self.keys:
                self.add_key(key)

        for key in self.keys:
            if key not in dict_value:
                dict_value[key] = np.nan

        self.db = self.db.append([dict_value], ignore_index=True)

    def modify_value(self, index, dict_value):
        self.db.loc[index] = dict_value

    def del_value(self, index):
        if isinstance(key, list):
            self.db.drop(index=index)
        else:
            self.db.drop(index=[index])
    
    def show(self):
        print(self.db)

    def save(self, path=''):
        if len(path) > 0:
            self.db_path = path
        self.db.to_hdf(self.db_path, self.db_name)

    def load(self):
        self.db = pd.read_hdf(self.db_path, self.db_name)