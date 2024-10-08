import time
import tracemalloc
import os
import heapq
from contextlib import ExitStack

# Ram is 16 MB
chunk_size = 0.5 # 16 MB
chunk = []
number_of_lines_per_chunk = chunk_size * 1024 * 1024 // 8  # 8 bytes per number
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
    merge_time_end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    peak_mb = peak / 1024 / 1024
    details.append('merge memory usage: '+ str(peak_mb)+ 'MB')
    details.append('merge time: '+ str(round(merge_time_end - merge_time_start, 2))+ 'seconds')
    tracemalloc.stop()

# Function to find the partition position
def partition(array, low, high):

    # Choose the rightmost element as pivot
    pivot = array[high]

    # Pointer for greater element
    i = low - 1

    # Traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:

            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1

            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])

    # Swap the pivot element with
    # the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])

    # Return the position from where partition is done
    return i + 1

# Function to perform quicksort
def quicksort(array, low, high):
    if low < high:

        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high)

        # Recursive call on the left of pivot
        quicksort(array, low, pi - 1)

        # Recursive call on the right of pivot
        quicksort(array, pi + 1, high)

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
            chunk.append(int(line))
            if len(chunk) == number_of_lines_per_chunk:
                quicksort(chunk, 0, len(chunk) - 1)
                with open('chunk' + str(chunk_count) + '.txt', 'w') as chunk_file:
                    for number in chunk:
                        chunk_file.write(str(number) + '\n')
                chunk.clear()
                # print('Chunk ' + str(chunk_count) + ' stored!')
                chunk_count += 1

                # print_memory_usage()
    
    # Write any remaining lines in the last chunk
    if chunk:
        with open('chunk' + str(chunk_count) + '.txt', 'w') as chunk_file:
            for number in chunk:
                chunk_file.write(str(number) + '\n')
        chunk.clear()
        print('Chunk ' + str(chunk_count) + ' stored!')
        chunk_count += 1
        
        print_memory_usage()

    
    current, peak = tracemalloc.get_traced_memory()
    peak_mb = peak / 1024 / 1024
    split_end = time.time()
    details.append('split memory usage: '+ str(peak_mb)+ 'MB')
    details.append('split time: '+ str(round(split_end - split_start, 2))+ 'seconds')

    # stopping the library
    tracemalloc.stop()
    return chunk_count

def delete_files(n_chunks):
    for i in range(n_chunks):
        file_name = 'chunk' + str(i) + '.txt'
        os.remove(file_name)

def logDetails(time_taken):
    with open('details_quick'+str(chunk_size)+'.txt', 'w') as file:
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
    print("")
    print('File split and chunks stored successfully!')
    print('Number of chunks: ' + str(n_chunks))
    print("")
    print("---------------------------------------------")
    print("")
    
    print("---------------------------------------------")
    print("")
    print('Chunks sorted successfully!')
    print("")
    print("---------------------------------------------")
    print('Merging sorted chunks...')

    sorted_files = [f'chunk{i}.txt' for i in range(n_chunks)]
    print(sorted_files)
    k_way_merge(sorted_files, 'sorted_quick.txt')
    delete_files(n_chunks)


    end_time = time.time()
    logDetails(round(end_time - start_time, 2))
    print('Time elapsed: ' + str(round(end_time - start_time, 2)) + ' seconds')
