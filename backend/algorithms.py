
def bubble_sort(arr):
    n = len(arr)
    comparisons = 0
    swaps = 0
    a = arr[:]
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return a, comparisons, swaps

def selection_sort(arr):
    n = len(arr)
    comparisons = 0
    swaps = 0
    a = arr[:]
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
    return a, comparisons, swaps

def insertion_sort(arr):
    n = len(arr)
    comparisons = 0
    moves = 0
    a = arr[:]
    for i in range(1, n):
        key = a[i]
        j = i - 1
        comparisons_in_loop = 0
        while j >= 0:
            comparisons_in_loop += 1
            if key < a[j]:
                a[j + 1] = a[j]
                moves += 1
                j -= 1
            else:
                break
        comparisons += comparisons_in_loop
        a[j + 1] = key
        moves += 1
    return a, comparisons, moves

def merge_sort(arr):
    a = arr[:]
    comparisons = 0
    moves = 0
    def _merge_sort_recursive(sub_array):
        nonlocal comparisons, moves
        if len(sub_array) <= 1: return sub_array
        mid = len(sub_array) // 2
        left_half, right_half = _merge_sort_recursive(sub_array[:mid]), _merge_sort_recursive(sub_array[mid:])
        merged, i, j = [], 0, 0
        while i < len(left_half) and j < len(right_half):
            comparisons += 1
            if left_half[i] < right_half[j]: merged.append(left_half[i]); i += 1
            else: merged.append(right_half[j]); j += 1
            moves += 1
        merged.extend(left_half[i:])
        moves += len(left_half[i:])
        merged.extend(right_half[j:])
        moves += len(right_half[j:])
        return merged
    return _merge_sort_recursive(a), comparisons, moves

def quick_sort(arr):
    a = arr[:]
    comparisons, swaps = 0, 0
    def _partition(sub_array, low, high):
        nonlocal comparisons, swaps
        pivot, i = sub_array[high], low - 1
        for j in range(low, high):
            comparisons += 1
            if sub_array[j] <= pivot:
                i += 1
                sub_array[i], sub_array[j] = sub_array[j], sub_array[i]
                swaps += 1
        sub_array[i + 1], sub_array[high] = sub_array[high], sub_array[i + 1]
        swaps += 1
        return i + 1
    def _quick_sort_recursive(sub_array, low, high):
        if low < high:
            pi = _partition(sub_array, low, high)
            _quick_sort_recursive(sub_array, low, pi - 1)
            _quick_sort_recursive(sub_array, pi + 1, high)
    _quick_sort_recursive(a, 0, len(a) - 1)
    return a, comparisons, swaps

def heap_sort(arr):
    a = arr[:]
    n = len(a)
    comparisons, swaps = 0, 0
    def _heapify(sub_array, n_heap, i):
        nonlocal comparisons, swaps
        largest, left, right = i, 2 * i + 1, 2 * i + 2
        if left < n_heap:
            comparisons += 1
            if sub_array[left] > sub_array[largest]: largest = left
        if right < n_heap:
            comparisons += 1
            if sub_array[right] > sub_array[largest]: largest = right
        if largest != i:
            sub_array[i], sub_array[largest] = sub_array[largest], sub_array[i]
            swaps += 1
            _heapify(sub_array, n_heap, largest)
    for i in range(n // 2 - 1, -1, -1): _heapify(a, n, i)
    for i in range(n - 1, 0, -1):
        a[i], a[0] = a[0], a[i]
        swaps += 1
        _heapify(a, i, 0)
    return a, comparisons, swaps

def counting_sort(arr):
    if not arr or min(arr) < 0: return arr, 0, 0
    max_val = max(arr)
    m = max_val + 1
    count = [0] * m
    output = [0] * len(arr)
    accesses = 0
    for x in arr: count[x] += 1; accesses += 2
    for i in range(1, m): count[i] += count[i-1]; accesses += 2
    for i in range(len(arr) - 1, -1, -1):
        val = arr[i]
        pos = count[val] - 1
        output[pos] = val
        count[val] -= 1
        accesses += 6
    return output, 0, accesses

# Dictionary to map algorithm names to functions
ALGORITHMS = {
    "Bubble Sort": bubble_sort, "Selection Sort": selection_sort, "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort, "Quick Sort": quick_sort, "Heap Sort": heap_sort, "Counting Sort": counting_sort,
}

ALGORITHM_METADATA = {
    "Bubble Sort": {"time_best": "Ω(n)", "time_avg": "Θ(n^2)", "time_worst": "O(n^2)", "space": "O(1)"},
    "Selection Sort": {"time_best": "Ω(n^2)", "time_avg": "Θ(n^2)", "time_worst": "O(n^2)", "space": "O(1)"},
    "Insertion Sort": {"time_best": "Ω(n)", "time_avg": "Θ(n^2)", "time_worst": "O(n^2)", "space": "O(1)"},
    "Merge Sort": {"time_best": "Ω(n log n)", "time_avg": "Θ(n log n)", "time_worst": "O(n log n)", "space": "O(n)"},
    "Quick Sort": {"time_best": "Ω(n log n)", "time_avg": "Θ(n log n)", "time_worst": "O(n^2)", "space": "O(log n)"},
    "Heap Sort": {"time_best": "Ω(n log n)", "time_avg": "Θ(n log n)", "time_worst": "O(n log n)", "space": "O(1)"},
    "Counting Sort": {"time_best": "Ω(n+k)", "time_avg": "Θ(n+k)", "time_worst": "O(n+k)", "space": "O(k)"},
}
