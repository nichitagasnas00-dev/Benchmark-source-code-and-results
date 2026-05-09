import random
import time
import string
import heapq
import sys
from multiprocessing import Pool, cpu_count

sys.setrecursionlimit(20000)




def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def array_to_linked_list(arr):
    if not arr: return None
    head = Node(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = Node(val)
        curr = curr.next
    return head

def get_middle(head):
    if not head: return head
    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    return slow

def sorted_merge(a, b):
    if not a: return b
    if not b: return a
    if a.val <= b.val:
        result = a
        result.next = sorted_merge(a.next, b)
    else:
        result = b
        result.next = sorted_merge(a, b.next)
    return result

def merge_sort_linked_list(head):
    if not head or not head.next:
        return head
    middle = get_middle(head)
    next_to_middle = middle.next
    middle.next = None
    left = merge_sort_linked_list(head)
    right = merge_sort_linked_list(next_to_middle)
    return sorted_merge(left, right)


def parallel_sort_worker(arr):
    return sorted(arr)

def parallel_merge_sort(arr):
    cores = cpu_count()
    if len(arr) < 10000 or cores < 2:
        return sorted(arr)
    
    chunk_size = len(arr) // cores
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    
    with Pool(cores) as pool:
        sorted_chunks = pool.map(parallel_sort_worker, chunks)
    
    while len(sorted_chunks) > 1:
        merged = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                left, right = sorted_chunks[i], sorted_chunks[i+1]
                res = []
                x = y = 0
                while x < len(left) and y < len(right):
                    if left[x] < right[y]:
                        res.append(left[x])
                        x += 1
                    else:
                        res.append(right[y])
                        y += 1
                res.extend(left[x:])
                res.extend(right[y:])
                merged.append(res)
            else:
                merged.append(sorted_chunks[i])
        sorted_chunks = merged
    return sorted_chunks[0]

def data_stream_generator(arr):
    for item in arr:
        yield item

def stream_sort(stream, chunk_size=10000):
    chunks = []
    current_chunk = []
    for item in stream:
        current_chunk.append(item)
        if len(current_chunk) >= chunk_size:
            chunks.append(sorted(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(sorted(current_chunk))
    return list(heapq.merge(*chunks))

#data structures
def generate_base_array(size, dtype):
    if dtype == 'int': return [random.randint(0, size) for _ in range(size)]
    elif dtype == 'float': return [random.uniform(0, size) for _ in range(size)]
    elif dtype == 'string': return [''.join(random.choices(string.ascii_letters, k=5)) for _ in range(size)]

def apply_structure(arr, structure):
    size = len(arr)
    if structure == 'random':
        return arr
    elif structure == 'sorted':
        return sorted(arr)
    elif structure == 'reverse':
        return sorted(arr, reverse=True)
    elif structure == 'almost':
        arr = sorted(arr)
        swaps = max(1, int(size * 0.02)) 
        for _ in range(swaps):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    elif structure == 'mixed':
        arr = sorted(arr)
        mid = size // 2
        second_half = arr[mid:]
        random.shuffle(second_half)
        return arr[:mid] + second_half
    elif structure == 'flat':
        distinct_vals = [arr[0], arr[size//2], arr[-1]]
        return [random.choice(distinct_vals) for _ in range(size)]

#engine
def run_benchmark():
    small_sizes = [20, 30, 50, 100]
    small_iterations = 100000
    medium_sizes = [1000, 10000]
    large_sizes = [1000000]
    all_sizes = small_sizes + medium_sizes + large_sizes
    
    dtypes = ['int', 'float', 'string']
    structures = ['random', 'sorted', 'reverse', 'almost', 'mixed', 'flat']
    
    for size in all_sizes:
        print(f"\n{'='*50}\nTesting Size: {size}\n{'='*50}")
        iterations = small_iterations if size in small_sizes else 1
        
        for dtype in dtypes:
            for struct in structures:
                if struct == 'flat' and size < 100000:
                    continue
                
                print(f"\n  -> Data Type: {dtype.upper()} | Structure: {struct.upper()}")
                
                
                test_data_batch = [apply_structure(generate_base_array(size, dtype), struct) for _ in range(iterations)]
                
                def measure_algo(name, algo_func, skip_if_large=False):
                    if skip_if_large and size > 1000:
                        print(f"     - {name}: [SKIPPED - O(n^2) too slow for size > 1000]")
                        return
                    
                    batch_copy = [arr[:] for arr in test_data_batch]
                    start_time = time.time()
                    for data in batch_copy:
                        algo_func(data)
                    print(f"     - {name}: {(time.time() - start_time):.4f} seconds")

               
                measure_algo("Quick Sort", quick_sort)
                measure_algo("Merge Sort (Array)", merge_sort)
                measure_algo("Insertion Sort", insertion_sort, skip_if_large=True)
                measure_algo("Bubble Sort", bubble_sort, skip_if_large=True)
                measure_algo("Selection Sort", selection_sort, skip_if_large=True)
                
                # Linked List Sort
                if size <= 10000:
                    ll_batch = [array_to_linked_list(arr[:]) for arr in test_data_batch]
                    start_time = time.time()
                    for ll_head in ll_batch:
                        _ = merge_sort_linked_list(ll_head)
                    print(f"     - Merge Sort (Linked List): {(time.time() - start_time):.4f} seconds")
                else:
                    print("     - Merge Sort (Linked List): [SKIPPED - Size too large for Python recursion]")
                
                # Parallel Sort
                if size >= 10000:
                    batch_copy = [arr[:] for arr in test_data_batch]
                    start_time = time.time()
                    for data in batch_copy:
                        _ = parallel_merge_sort(data)
                    print(f"     - Parallel Merge Sort: {(time.time() - start_time):.4f} seconds")
                    
                # Stream Sort
                start_time = time.time()
                for data in test_data_batch:
                    stream = data_stream_generator(data)
                    _ = stream_sort(stream)
                print(f"     - Stream Sort (Heap): {(time.time() - start_time):.4f} seconds")

if __name__ == "__main__":
    print("Starting Comprehensive Sort Benchmark...")
    run_benchmark()
    print("\nBenchmark Complete.")