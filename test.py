from cache_to_db_decorater import *

@cache_to_db
def f():
    return 1

f()
f()