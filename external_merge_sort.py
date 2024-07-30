import time
import tracemalloc
import os
import heapq
from contextlib import ExitStack

def k_way_merge(sorted_files, output_file):
    tracemalloc.start()
    print_memory_usage()

    with ExitStack() as stack:
        # Open all files and keep them open
        files = [stack.enter_context(open(f)) for f in sorted_files]
        
        # Initialize the heap with the first element from each file
        heap = []
        for file_idx, file in enumerate(files):
            line = file.readline().strip()
            if line:
                heapq.heappush(heap, (int(line), file_idx))
        
        with open(output_file, 'w') as out:
            while heap:
                smallest, file_idx = heapq.heappop(heap)
                out.write(f"{smallest}\n")
                
                # Read the next line from the file
                line = files[file_idx].readline().strip()
                if line:
                    heapq.heappush(heap, (int(line), file_idx))
    
    print('Chunks merged successfully!')
    print_memory_usage()    
    tracemalloc.stop()

# Merge sort

def merge(arr, start, mid, end):
    start2 = mid + 1
 
    # If the direct merge is already sorted
    if (arr[mid] <= arr[start2]):
        return
 
    # Two pointers to maintain start
    # of both arrays to merge
    while (start <= mid and start2 <= end):
 
        # If element 1 is in right place
        if (arr[start] <= arr[start2]):
            start += 1
        else:
            value = arr[start2]
            index = start2
 
            # Shift all the elements between element 1
            # element 2, right by 1.
            while (index != start):
                arr[index] = arr[index - 1]
                index -= 1
 
            arr[start] = value
 
            # Update all the pointers
            start += 1
            mid += 1
            start2 += 1
 
 
'''
* l is for left index and r is right index of
the sub-array of arr to be sorted
'''
 
 
def mergeSort(arr, l, r):
    if (l < r):
 
        # Same as (l + r) / 2, but avoids overflow
        # for large l and r
        m = l + (r - l) // 2
 
        # Sort first and second halves
        mergeSort(arr, l, m)
        mergeSort(arr, m + 1, r)
 
        merge(arr, l, m, r)

# Ram is 16 MB
chunk_size = 4 # 16 MB
chunk = []
number_of_lines_per_chunk = chunk_size * 1024 * 1024 // 8  # 8 bytes per number

def print_memory_usage():
    current, peak = tracemalloc.get_traced_memory()

    # Convert to MB
    current_mb = current / 1024 / 1024
    peak_mb = peak / 1024 / 1024

    # Print the results in MB
    print(f"Current memory usage: {current_mb:.2f} MB")
    print(f"Peak memory usage: {peak_mb:.2f} MB")

def split_file():
    # starting the monitoring
    tracemalloc.start()

    print('Splitting file into chunks and sorting...')
    
    print_memory_usage()
    
    chunk_count = 0
    with open('unsorted.txt', 'r') as file:
        for line in file:
            chunk.append(int(line))
            if len(chunk) == number_of_lines_per_chunk:
                
                mergeSort(chunk, 0, len(chunk) - 1)
                
                with open('chunk' + str(chunk_count) + '.txt', 'w') as chunk_file:
                    for number in chunk:
                        chunk_file.write(str(number) + '\n')
                chunk.clear()
                print('Chunk ' + str(chunk_count) + ' stored!')
                chunk_count += 1

                print_memory_usage()
    
    # Write any remaining lines in the last chunk
    if chunk:
        with open('chunk' + str(chunk_count) + '.txt', 'w') as chunk_file:
            for number in chunk:
                chunk_file.write(str(number) + '\n')
        chunk.clear()
        print('Chunk ' + str(chunk_count) + ' stored!')
        chunk_count += 1
        
        print_memory_usage()

    # stopping the library
    tracemalloc.stop()
    return chunk_count

def delete_files(n_chunks):
    for i in range(n_chunks):
        file_name = 'chunk' + str(i) + '.txt'
        os.remove(file_name)

if __name__ == '__main__':
    # record the start time
    start_time = time.time()

    # split file into chunks and sort individual chunks
    
    
    n_chunks = split_file()
    
    print("---------------------------------------------")
    print("")
    print('File split and chunks stored successfully!')
    print('Number of chunks: ' + str(n_chunks))
    print("")
    print("---------------------------------------------")

    
    print('Merging sorted chunks...')

    sorted_files = [f'chunk{i}.txt' for i in range(n_chunks)]
    print(sorted_files)
    k_way_merge(sorted_files, 'sorted_merge.txt')
    
    delete_files(n_chunks)

    end_time = time.time()
    print('Time elapsed: ' + str(round(end_time - start_time, 2)) + ' seconds')
