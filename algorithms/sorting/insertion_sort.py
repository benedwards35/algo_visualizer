def insertion_sort(array):
    arr = array[:]
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        state = {"i": i, "key": key, "j": j, "n": n}
        yield arr, (i,), 4, state
        while j >= 0 and key < arr[j]:
            arr[j+1] = arr[j]
            state = {"i": i, "key": key, "j": j, "n": n}
            yield arr, (j, j+1), 7, state
            j -= 1
        arr[j+1] = key
        state = {"i": i, "key": key, "j": j, "n": n}
        yield arr, (j+1,), 10, state
    state = {"i": n, "key": 0, "j": 0, "n": n}
    yield arr, None, 11, state