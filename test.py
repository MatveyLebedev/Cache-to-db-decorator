from cache_to_db_decorator import *

settings(drop_table=False)
@cache_to_db
def f():
    return 1

f()
f()