'''This decorator is developed to easily cache any type of data, if input data can be converted to a string'''

import sqlite3
import pickle
import os

'''default settings'''

pach = 'cached_files'
drop_table = True
db_name = 'db_cache'

'''function for setting data base parameters'''

def settings(**kwargs):
    global pach, drop_table, table_name, db_name
    if 'pach' in kwargs: pach = kwargs['pach']
    if 'drop_table' in kwargs: drop_table = kwargs['drop_table']
    if 'table_name' in kwargs: table_name = kwargs['table_name']
    if 'db_name' in kwargs: db_name = kwargs['db_name']


''' This decorator is caching data from function call (input, and output) at data base,
    input is storing as a string, and output is storing as a dump of python object'''

class cache_to_db(object):
    def __init__(self, f):
        global pach, drop_table, db_name
        self.f = f
        try:
            assert os.access(pach, os.W_OK) is True
        except AssertionError:
            os.mkdir(pach)
        self.pach = pach
        self.table_name = f.__name__
        self.conn = sqlite3.connect(f'{db_name}.sqlite')
        self.cur = self.conn.cursor()
        self.caunter = 0
        if drop_table is True:
            self.cur.execute(f'DROP TABLE IF EXISTS {self.table_name}')
            self.cur.execute(f'CREATE TABLE {self.table_name} (inp TEXT PRIMARY KEY, out TEXT)')
        else:
            if len(tuple(self.cur.execute(f'''
            SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}' '''))) == 0:
                self.cur.execute(f'CREATE TABLE {self.table_name} (inp TEXT PRIMARY KEY, out TEXT)')
        self.caunter = tuple(self.cur.execute(f'SELECT COUNT(*) FROM {self.table_name}'))[0][0]
        self.conn.commit()
        try:
            assert os.access(self.pach + '/' + self.table_name, os.W_OK) is True
        except AssertionError:
            os.mkdir(self.pach + '/' + self.table_name)

    def __call__(self, *args, **kwargs):
        inp = (args, kwargs,)
        out = tuple(self.cur.execute(f'''SELECT * FROM {self.table_name} WHERE inp=?''', (str(inp), )))
        if len(out) == 1:
            pach_out = out[0][1]
            with open(pach_out, 'rb') as f:
                return pickle.load(f)
        else:
            out = self.f(*args, **kwargs)
            nuw_pach = self.pach + '/' + self.table_name + '/' + f'{self.caunter}'
            with open(nuw_pach, 'wb') as f:
                pickle.dump(out, f)
            self.cur.execute(f'INSERT INTO {self.table_name} (inp, out) VALUES (?, ?)', (str(inp), nuw_pach))
            self.conn.commit()
            self.caunter += 1
            return out
