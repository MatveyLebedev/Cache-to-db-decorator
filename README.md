# Cache-to-db-decorator
This decorator is developed to easily cache any type of data on condition that input data can be converted to a string.
You can use the decorator to decrease time of your program running if it repeatedly uses  slow data sources.
It can simplify your program logic and debugging process.
To use this library you just need to add @cache_to_db decorator to your function.
To change your settings you should use the settings function. 

It has the following arguments: 

pach = 'cached_files'

drop_table = True

table_name = 'Dump'

db_name = 'db_cache'

Example:

@cache_to_db
def caunt_cache(arr):
    for i in range(len(arr)):
        arr[i] = arr[i] ** 2
    return arr

def caunt(arr):
    for i in range(len(arr)):
        arr[i] = arr[i] ** 2
    return arr

assert caunt_cache([1, 2, 3]) == caunt([1, 2, 3])
