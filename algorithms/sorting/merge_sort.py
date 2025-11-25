def merge_sort(array):
    arr = array[:]
    n = len(arr)
    
    def rec(arr, left, right):
        if left == right:
            return
        mid = (left + right) // 2
        yield from rec(arr, left, mid)
        yield from rec(arr, mid+1, right)
        
        left_temp = arr[left:mid+1]
        right_temp = arr[mid+1:right+1]
        i, j = 0, 0
        k = left
        
        while i < len(left_temp) and j < len(right_temp):
            if left_temp[i] < right_temp[j]:
                arr[k] = left_temp[i]
                i += 1
            else:
                arr[k] = right_temp[j]
                j += 1
            state = {"k": k, "n": n, "phase": "merge"}
            yield arr, (k,), 18, state
            k += 1
            
        while i < len(left_temp):
            arr[k] = left_temp[i]
            state = {"k": k, "n": n, "phase": "copy_left"}
            yield arr, (k,), 22, state
            i += 1
            k += 1
            
        while j < len(right_temp):
            arr[k] = right_temp[j]
            state = {"k": k, "n": n, "phase": "copy_right"}
            yield arr, (k,), 27, state
            j += 1
            k += 1
    
    yield from rec(arr, 0, len(arr)-1)
    state = {"k": n, "n": n, "phase": "complete"}
    yield arr, None, 31, state