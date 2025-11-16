def bubble_sort(array):

    n = len(array)
    arr = array[:]  
    for i in range(n):
        for j in range(n - i - 1):
            yield arr, (j, j + 1)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr, (j, j + 1)
    yield arr, None