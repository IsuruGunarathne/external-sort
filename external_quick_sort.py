import time
import tracemalloc

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Ram is 16 MB
chunk_size = 16 # 16 MB
chunk = []
number_of_lines_per_chunk = chunk_size * 1024 * 1024 // 8  # 8 bytes per number


def split_sort_file():
    # starting the monitoring
    tracemalloc.start()

    print('Splitting file into chunks and sorting...')
    
    # print memory usage at start
    current, peak = tracemalloc.get_traced_memory()
    print(f"Initial memory usage: {current / 1024 / 1024} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024} MB")
    
    chunk_count = 0
    with open('unsorted.txt', 'r') as file:
        for line in file:
            chunk.append(int(line))
            if len(chunk) == number_of_lines_per_chunk:
                quicksort(chunk)
                with open('chunk' + str(chunk_count) + '.txt', 'w') as chunk_file:
                    for number in chunk:
                        chunk_file.write(str(number) + '\n')
                chunk.clear()
                print('Chunk ' + str(chunk_count) + ' sorted and stored!')
                chunk_count += 1

                # Get the current and peak memory usage
                current, peak = tracemalloc.get_traced_memory()

                # Convert to MB
                current_mb = current / 1024 / 1024
                peak_mb = peak / 1024 / 1024

                # Print the results in MB
                print(f"Current memory usage: {current_mb:.2f} MB")
                print(f"Peak memory usage: {peak_mb:.2f} MB")
    

    # stopping the library
    tracemalloc.stop()


if __name__ == '__main__':
    # record the start time
    start_time = time.time()

    # split file into chunks and sort individual chunks
    split_sort_file()
    print('File split and chunks sorted successfully!')

    # merge_files()
    # print('File sorted successfully!')

    end_time = time.time()
    print('Time elapsed: ' + str(round(end_time - start_time, 2)) + ' seconds')
