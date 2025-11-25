def bubble_sort(array):
    n = len(array)
    arr = array[:]
    for i in range(n):
        for j in range(n - i - 1):
            state = {"outer_i": i, "inner_j": j, "n": n}
            yield arr, (j, j+1), 5, state
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                state = {"outer_i": i, "inner_j": j, "n": n}
                yield arr, (j, j+1), 7, state
    state = {"outer_i": n, "inner_j": 0, "n": n}
    yield arr, None, 9, state