# Chache-to-db-decorator
This decorator is developed to easily cache any type of data, if input data can be converted to a string.

Yuy can use it to decrease time of yor program running if it using slow data sores wise same requests,
it can simplify yor program logic and debugging process.

For using this library you just need to add @cache_to_db decorator to yor function.

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
