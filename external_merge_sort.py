import time
import tracemalloc
import os
import heapq
from contextlib import ExitStack

# Ram is 16 MB
chunk_size = 0.5  # 16 MB
chunk = []
number_of_lines_per_chunk = int(chunk_size * 1024 * 1024 // 8)  # 8 bytes per number
details = []

def k_way_merge(sorted_files, output_file):
    merge_time_start = time.time()
    tracemalloc.start()
    print_memory_usage()

    with ExitStack() as stack:
        # Open all files and keep them open
        files = [stack.enter_context(open(f)) for f in sorted_files]

        # Initialize the heap with the first element from each file
        heap = []
        for file_idx, file in enumerate(files):
            line = file.readline().strip()
            if line:  # Avoid empty lines
                heapq.heappush(heap, (int(line), file_idx))

        with open(output_file, 'w') as out:
            while heap:
                smallest, file_idx = heapq.heappop(heap)
                out.write(f"{smallest}\n")

                # Read the next line from the file
                line = files[file_idx].readline().strip()
                if line:  # Avoid empty lines
                    heapq.heappush(heap, (int(line), file_idx))

    print('Chunks merged successfully!')
    print_memory_usage()
    merge_time_end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    peak_mb = peak / 1024 / 1024
    details.append('merge memory usage: ' + str(peak_mb) + 'MB')
    details.append('merge time: ' + str(round(merge_time_end - merge_time_start, 2)) + ' seconds')
    tracemalloc.stop()

# Merge sort

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Divide the array into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # Recursively sort both halves
    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    # Merge the sorted halves
    return merge(left_sorted, right_sorted)

def merge(left, right):
    merged = []
    left_index = 0
    right_index = 0

    # Merge the two halves together while maintaining order
    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    # If there are remaining elements in the left half, add them
    while left_index < len(left):
        merged.append(left[left_index])
        left_index += 1

    # If there are remaining elements in the right half, add them
    while right_index < len(right):
        merged.append(right[right_index])
        right_index += 1

    return merged

def print_memory_usage():
    current, peak = tracemalloc.get_traced_memory()

    # Convert to MB
    current_mb = current / 1024 / 1024
    peak_mb = peak / 1024 / 1024

    # Print the results in MB
    print(f"Current memory usage: {current_mb:.2f} MB")
    print(f"Peak memory usage: {peak_mb:.2f} MB")

def split_file():
    split_start = time.time()
    # starting the monitoring
    tracemalloc.start()

    print('Splitting file into chunks and sorting...')

    print_memory_usage()

    chunk_count = 0
    with open('unsorted.txt', 'r') as file:
        for line in file:
            line = line.strip()  # Avoid empty lines
            if line:
                chunk.append(int(line))
            if len(chunk) == number_of_lines_per_chunk:
                sorted_chunk = merge_sort(chunk)

                with open('chunk' + str(chunk_count) + '.txt', 'w') as chunk_file:
                    for number in sorted_chunk:
                        chunk_file.write(str(number) + '\n')
                chunk.clear()
                chunk_count += 1

    # Write any remaining lines in the last chunk
    if chunk:
        sorted_chunk = merge_sort(chunk)  # Sort the remaining chunk
        with open('chunk' + str(chunk_count) + '.txt', 'w') as chunk_file:
            for number in sorted_chunk:
                chunk_file.write(str(number) + '\n')
        chunk.clear()
        chunk_count += 1

    print_memory_usage()

    split_end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    peak_mb = peak / 1024 / 1024
    details.append('split memory usage: ' + str(peak_mb) + 'MB')
    details.append('split time: ' + str(round(split_end - split_start, 2)) + ' seconds')
    tracemalloc.stop()
    return chunk_count

def delete_files(n_chunks):
    for i in range(n_chunks):
        file_name = 'chunk' + str(i) + '.txt'
        os.remove(file_name)

def log_details(time_taken):
    with open('details_merge' + str(chunk_size) + '.txt', 'w') as file:
        file.write('Details:\n')
        file.write('---------------------------------------------\n')
        file.write('Chunk size: ' + str(chunk_size) + ' MB\n')
        file.write('Number of lines per chunk: ' + str(number_of_lines_per_chunk) + '\n')
        file.write('---------------------------------------------\n')
        for detail in details:
            file.write(str(detail) + '\n')
        file.write('---------------------------------------------\n')
        file.write('Total Time taken: ' + str(time_taken) + ' seconds\n')

if __name__ == '__main__':
    # record the start time
    start_time = time.time()

    # split file into chunks and sort individual chunks
    n_chunks = split_file()

    print("---------------------------------------------")
    print('File split and chunks stored successfully!')
    print('Number of chunks: ' + str(n_chunks))
    print("---------------------------------------------")

    print('Merging sorted chunks...')

    sorted_files = [f'chunk{i}.txt' for i in range(n_chunks)]
    k_way_merge(sorted_files, 'sorted_merge.txt')
    delete_files(n_chunks)

    end_time = time.time()
    log_details(round(end_time - start_time, 2))
    print('Time elapsed: ' + str(round(end_time - start_time, 2)) + ' seconds')
