def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        yield arr, (i,)
        
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            yield arr, (j, j+1)
            j -= 1

        arr[j+1] = key
        yield arr, (j+1,)

    yield arr, None


