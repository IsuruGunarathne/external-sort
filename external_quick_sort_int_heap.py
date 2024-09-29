# Imports
import time
import tracemalloc
import math
import os

# Interval heap

class IntervalHeap:
    def __init__(self,array):
        self.min_heap = []
        self.max_heap = []
        self.buildHeap(array, len(array))
    def maxHeapifyUp(self,arr, i):
        parent = (i - 1) // 2
        if parent >= 0 and arr[i] > arr[parent]:
            (arr[i], arr[parent]) = (arr[parent], arr[i])
            self.maxHeapifyUp(arr, parent)
    def minHeapifyUp(self,arr, i):
        parent = (i - 1) // 2
        if parent >= 0 and arr[i] < arr[parent]:
            (arr[i], arr[parent]) = (arr[parent], arr[i])
            self.minHeapifyUp(arr, parent)
    def maxHeapifyDown(self,arr, n, i):
        largest = i  
        l = 2 * i + 1  
        r = 2 * i + 2  
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        if largest != i:
            (arr[i], arr[largest]) = (arr[largest], arr[i])
            if self.min_heap[largest]> self.max_heap[largest]:
                self.min_heap[largest], self.max_heap[largest] = self.max_heap[largest], self.min_heap[largest]
            self.maxHeapifyDown(self.max_heap, len(self.max_heap), largest)

    def minHeapifyDown(self,arr, n, i):
        smallest = i  
        l = 2 * i + 1  
        r = 2 * i + 2  
        if l < n and arr[i] > arr[l]:
            smallest = l
        if r < n and arr[smallest] > arr[r]:
            smallest = r
        if smallest != i:
            (arr[i], arr[smallest]) = (arr[smallest], arr[i])
            if len(self.max_heap) > smallest and self.min_heap[smallest]> self.max_heap[smallest]:
                self.min_heap[smallest], self.max_heap[smallest] = self.max_heap[smallest], self.min_heap[smallest]
            self.minHeapifyDown(self.min_heap, len(self.min_heap), smallest)
    def insert(self, value):
        if len(self.min_heap) == len(self.max_heap) :
            self.min_heap.append(value)
            parent = (len(self.min_heap) - 2) // 2
            if parent >= 0 and self.max_heap[parent] < self.min_heap[-1]:
                self.max_heap[parent], self.min_heap[-1] = self.min_heap[-1], self.max_heap[parent]
                self.maxHeapifyUp(self.max_heap, parent)
            else:
                self.minHeapifyUp(self.min_heap, len(self.min_heap) - 1)
        elif len(self.min_heap) > len(self.max_heap):
            self.max_heap.append(value)
            if self.max_heap[-1] < self.min_heap[-1]:
                self.max_heap[-1], self.min_heap[-1] = self.min_heap[-1], self.max_heap[-1]
                self.minHeapifyUp(self.min_heap,len(self.min_heap) - 1)
            else:
                self.maxHeapifyUp(self.max_heap, len(self.max_heap) - 1)
        else:
            print("Error in insert")
            exit()
    def buildHeap(self,arr, n):
        for i in range(n):
            self.insert(arr[i])
    def getMin(self):
        if len(self.min_heap) == 0:
            return None
        return self.min_heap[0]
    def getMax(self):
        if len(self.max_heap) == 0:
            if len(self.min_heap)==1:
                return self.min_heap[0]
            else:
                return None
        else:
            return self.max_heap[0]
    def popMax(self):
        if len(self.max_heap) == 0:
            if len(self.min_heap) == 1:
                return self.min_heap.pop()
            else:
                return None
        max_val = self.max_heap[0]
        if len(self.max_heap) == len(self.min_heap):
            self.max_heap[0] = self.max_heap[-1]
            self.max_heap.pop()
            self.maxHeapifyDown(self.max_heap, len(self.max_heap), 0)
        elif len(self.max_heap) < len(self.min_heap):
            self.max_heap[0] = self.min_heap[-1]
            self.min_heap.pop()
            self.maxHeapifyDown(self.max_heap, len(self.max_heap), 0)
        else:
            print("Error in popMax")
            exit()
        # print("heap sizes min ",len(self.min_heap),"max ",len(self.max_heap))
        return max_val
    def popMin(self):
        if len(self.min_heap) == 0:
            return None
        min_val = self.min_heap[0]
        if len(self.min_heap) == len(self.max_heap):
            self.min_heap[0] = self.max_heap[-1]
            self.max_heap.pop()
            self.minHeapifyDown(self.min_heap, len(self.min_heap), 0)
        elif len(self.min_heap) > len(self.max_heap):
            self.min_heap[0] = self.min_heap[-1]
            self.min_heap.pop()
            self.minHeapifyDown(self.min_heap, len(self.min_heap), 0)
        else:
            print("Error in popMin")
            exit()
        return min_val
    
def print_binary_tree(arr):
    if not arr:
        return

    def print_whitespace(count):
        print(" " * count, end='')

    levels = math.ceil(math.log2(len(arr) + 1))
    max_width = 2**(levels - 1)

    index = 0
    for level in range(levels):
        level_nodes = 2**level
        if index >= len(arr):
            break

        spacing = max_width // level_nodes
        first_spacing = spacing // 2

        print_whitespace(first_spacing)
        for i in range(level_nodes):
            if index >= len(arr):
                break
            print(arr[index], end='')
            index += 1
            if i < level_nodes - 1:
                print_whitespace(spacing)
        print()  # New line for the next level


# Fill buffer with input values
def fill_buffer(file, buffer, current_position,size):
    buffer.clear()
    for i in range(size):
        line = file.readline().strip()
        if not line:
            break
        buffer.append(int(line))
    current_position = current_position + size
    return current_position

def print_memory_usage():
    current, peak = tracemalloc.get_traced_memory()

    # Convert to MB
    current_mb = current / 1024 / 1024
    peak_mb = peak / 1024 / 1024

    # Print the results in MB
    print(f"Current memory usage: {current_mb:.2f} MB")
    print(f"Peak memory usage: {peak_mb:.2f} MB")

def print_buffers(buffer_small, buffer_large, buffer_in):
    print("buffer_small",buffer_small.__len__())
    print("buffer_large",buffer_large.__len__())
    print("buffer_in",buffer_in.__len__())

def write_buffer_to_file(buffer, file):
    for i in buffer:
        file.write(str(i) + "\n")
    
def sort(directory):
    print("sorting",directory)
    # Buffer sizes
    global depth_counter

    buffer_size_mid=1*1024*1024
    buffer_size_small=256*1024
    buffer_size_large=256*1024
    buffer_size_in=256*1024
    
    # Other tracking variables
    current_position=0
    min_max_to_remove=0 # 0 remove min, 1 remove max
    input_file=directory+'\\unsorted.txt'

    # Make large and small folders if they don't exist
    os.makedirs(directory + '\\large', exist_ok=True)
    os.makedirs(directory + '\\small', exist_ok=True)
    large_file=directory+'\\large\\unsorted.txt'
    small_file=directory+'\\small\\unsorted.txt'
    mid_file=directory+'\\mid.txt'
    # make empty files / delete contents of files
    open(large_file, 'w').close()
    open(small_file, 'w').close()
    open(mid_file, 'w').close()
    input_file_open = open(input_file, 'r')
    buffer_mid = []
    buffer_small = []
    buffer_large = []
    buffer_in = []


    ## Sorting logic

    # Fill buffers mid and input

    current_position=fill_buffer(input_file_open, buffer_mid, current_position,buffer_size_mid)
    current_position=fill_buffer(input_file_open, buffer_in, current_position,buffer_size_in)    
    print("current_position",current_position*8/1024/1024,"MB")

    # Create interval heap for mid buffer
    mid_heap = IntervalHeap(buffer_mid)
    buffer_mid.clear()
    print_buffers(buffer_small, buffer_large, buffer_in)


    
    while len(buffer_in)>0:
        val = buffer_in.pop(0)
        # print("val",val)
        # print_buffers(buffer_small, buffer_large, buffer_in)


        # store buffers to files and clear if full
        if len(buffer_small)>=buffer_size_small-5:
            write_buffer_to_file(buffer_small, open(small_file, 'a'))
            buffer_small.clear()
        
        if len(buffer_large)>=buffer_size_large-5:
            write_buffer_to_file(buffer_large, open(large_file, 'a'))
            buffer_large.clear()

        # Add value to relevant buffer
        if val <= mid_heap.getMin():
            # print("adding to small buffer")
            buffer_small.append(val)
        elif val >= mid_heap.getMax():
            # print("adding to large buffer")
            buffer_large.append(val)
        else:
            # add to mid heap
            if min_max_to_remove==0:
                # print(mid_heap.getMin(),"moving to small buffer",val,"addded to mid heap")
                buffer_small.append(mid_heap.popMin())
                mid_heap.insert(val)
                min_max_to_remove=1
            
            else:
                # print(mid_heap.getMax(),"moving to large buffer",val,"addded to mid heap")
                buffer_large.append(mid_heap.popMax())
                mid_heap.insert(val)
                min_max_to_remove=0

            

        # fill buffer_in if empty
        if len(buffer_in)==0:
            current_position=fill_buffer(input_file_open, buffer_in, current_position,buffer_size_in)
            # print("current_position",current_position*8/1024/1024,"MB")
            # print(mid_heap.getMin(),mid_heap.getMax())
            # print_memory_usage()
            # print_buffers(buffer_small, buffer_large, buffer_in)
    
    # write remaining buffers to files
    write_buffer_to_file(buffer_small, open(small_file, 'a'))
    write_buffer_to_file(buffer_large, open(large_file, 'a'))
    
    # print("current_position",current_position*8/1024/1024,"MB")

    # store fill mid_buffer from mid_heap
    buffer_mid_out = []
    while mid_heap.getMin() is not None:
        val = mid_heap.popMin()
        # print(val)
        buffer_mid_out.append(val)
    
    # write mid buffer to file

    # print('sorting mid buffer, not required if the heap works properly')
    # buffer_mid_out.sort()
    write_buffer_to_file(buffer_mid_out, open(mid_file, 'a'))
    buffer_mid_out.clear()


    # close files
    input_file_open.close()
    print("-------------------------------------------")
    print("finished depth",depth_counter)
    depth_counter+=1
    print_memory_usage()
    print("-------------------------------------------")

    # recursively sort large and small folders only if the 'unsorted.txt' file is not empty in each folder
    if os.stat(large_file).st_size > 0:
        sort(directory + '\\large')
    if os.stat(small_file).st_size > 0:
        sort(directory + '\\small')
    
    # combining all sorted files
    print("combining sorted files")
    skip_small = False
    skip_large = False
    # check if a sorted.txt file exists in the directory before trying to read from it
    if not os.path.exists(directory + '\\small\\sorted.txt'):
        skip_small = True
    else:
        sorted_small = open(directory + '\\small\\sorted.txt', 'r')
    
    if not os.path.exists(directory + '\\large\\sorted.txt'):
        skip_large = True
    else:
        sorted_large = open(directory + '\\large\\sorted.txt', 'r')

    sorted_file = open(directory+'\\sorted.txt', 'w')

    buffer_in=[]
    
    # read from sorted small file, fill buffer_in, and write to sorted file when buffer is full, repeat until all lines are read
    while True:
        if skip_small:
            print("skipping small at", directory)
            break
        line = sorted_small.readline().strip()
        if not line:
            break
        buffer_in.append(int(line))
        if len(buffer_in) >= buffer_size_in:
            write_buffer_to_file(buffer_in, sorted_file)
            buffer_in.clear()

    # write remaining buffer_in to sorted file
    write_buffer_to_file(buffer_in, sorted_file)
    buffer_in.clear()

    # read from mid file, fill buffer_in, and write to sorted file when buffer is full, repeat until all lines are read

    mid_open = open(mid_file, 'r')
    while True:
        line = mid_open.readline().strip()
        if not line:
            break
        buffer_in.append(int(line))
        if len(buffer_in) >= buffer_size_in:
            write_buffer_to_file(buffer_in, sorted_file)
            buffer_in.clear()

    # write remaining buffer_in to sorted file
    write_buffer_to_file(buffer_in, sorted_file)
    buffer_in.clear()

    # read from sorted large file, fill buffer_in, and write to sorted file when buffer is full, repeat until all lines are read
    while True:
        if skip_large:
            print("skipping large at",directory)
            break
        line = sorted_large.readline().strip()
        if not line:
            break
        buffer_in.append(int(line))
        if len(buffer_in) >= buffer_size_in:
            write_buffer_to_file(buffer_in, sorted_file)
            buffer_in.clear()
        
    # write remaining buffer_in to sorted file
    write_buffer_to_file(buffer_in, sorted_file)
    buffer_in.clear()

    # close files
    if not skip_small:
        sorted_small.close()
    if not skip_large:
        sorted_large.close()
    
    mid_open.close()
    sorted_file.close()

    # delete files
    if not skip_small:
        os.remove(directory + '\\small\\sorted.txt')
    if not skip_large:
        os.remove(directory + '\\large\\sorted.txt')
    os.remove(large_file)
    os.remove(small_file)
    os.remove(mid_file)

    print("finished sorting",directory)
    print("recursive depth",depth_counter)
    print_buffers(buffer_small, buffer_large, buffer_in)

if __name__ == '__main__':
    start_time = time.time()
    tracemalloc.start()
    
    depth_counter = 0

    # get current directory
    current_directory = os.getcwd()
    sort(current_directory)
    

    end_time = time.time()
    print_memory_usage()
    print(f"Execution time: {end_time - start_time:.2f} seconds ")
    tracemalloc.stop()

