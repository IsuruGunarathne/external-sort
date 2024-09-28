# Imports
import time
import tracemalloc
import math

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
        # print("Max Heapify Down")
        # print_binary_tree(self.min_heap)
        # print_binary_tree(self.max_heap)
        largest = i  
        l = 2 * i + 1  
        r = 2 * i + 2  
        if l < n and arr[i] < arr[l]:
            largest = l
        if r < n and arr[largest] < arr[r]:
            largest = r
        if largest != i:
            (arr[i], arr[largest]) = (arr[largest], arr[i])
            # Ensure that we're not accessing out-of-bound indices
            if largest < len(self.min_heap) and largest < len(self.max_heap):
                if self.min_heap[largest] > self.max_heap[largest]:
                    self.min_heap[largest], self.max_heap[largest] = self.max_heap[largest], self.min_heap[largest]
                    self.minHeapifyDown(self.min_heap, len(self.min_heap), largest)
            else:
                self.maxHeapifyDown(self.max_heap, len(self.max_heap), largest)

    def minHeapifyDown(self,arr, n, i):
        # print("Min Heapify Down")
        # print_binary_tree(self.min_heap)
        # print_binary_tree(self.max_heap)
        smallest = i  
        l = 2 * i + 1  
        r = 2 * i + 2  
        if l < n and arr[i] > arr[l]:
            smallest = l
        if r < n and arr[smallest] > arr[r]:
            smallest = r
        if smallest != i:
            (arr[i], arr[smallest]) = (arr[smallest], arr[i])
            if self.min_heap[smallest]> self.max_heap[smallest]:
                self.min_heap[smallest], self.max_heap[smallest] = self.max_heap[smallest], self.min_heap[smallest]
                self.maxHeapifyDown(self.max_heap, len(self.max_heap), smallest)
            else:
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
        else:
            self.max_heap.append(value)
            if self.max_heap[-1] < self.min_heap[-1]:
                self.max_heap[-1], self.min_heap[-1] = self.min_heap[-1], self.max_heap[-1]
                self.minHeapifyUp(self.min_heap,len(self.min_heap) - 1)
            else:
                self.maxHeapifyUp(self.max_heap, len(self.max_heap) - 1)
    def buildHeap(self,arr, n):
        for i in range(n):
            self.insert(arr[i])
    def getMin(self):
        if len(self.min_heap) == 0:
            return None
        return self.min_heap[0]
    def getMax(self):
        if len(self.max_heap) == 0:
            return None
        return self.max_heap[0]
    def popMax(self):
        # print("popMax")
        # print_binary_tree(self.min_heap)
        # print_binary_tree(self.max_heap)
        if len(self.max_heap) == 0:
            return None
        max_val = self.max_heap[0]
        if len(self.max_heap) >= len(self.min_heap):
            self.max_heap[0] = self.max_heap[-1]
            self.max_heap.pop()
            self.maxHeapifyDown(self.max_heap, len(self.max_heap), 0)
        else:
            self.max_heap[0] = self.min_heap[-1]
            self.min_heap.pop()
            self.maxHeapifyDown(self.max_heap, len(self.max_heap), 0)
        return max_val
    def popMin(self):
        # print("popMin")
        # print_binary_tree(self.min_heap)
        # print_binary_tree(self.max_heap)
        if len(self.min_heap) == 0:
            return None
        min_val = self.min_heap[0]
        if len(self.min_heap) >= len(self.max_heap):
            self.min_heap[0] = self.min_heap[-1]
            self.min_heap.pop()
            self.minHeapifyDown(self.min_heap, len(self.min_heap), 0)
        else:
            self.min_heap[0] = self.max_heap[-1]
            self.max_heap.pop()
            self.minHeapifyDown(self.min_heap, len(self.min_heap), 0)
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
    
if __name__ == '__main__':
    start_time = time.time()
    tracemalloc.start()
    # Buffer sizes

    buffer_size_mid=256*1024
    buffer_size_small=64*1024
    buffer_size_large=64*1024
    buffer_size_in=64*1024
    
    # Other tracking variables
    current_position=0
    min_max_to_remove=0 # 0 remove min, 1 remove max
    input_file='unsorted.txt'
    large_file='large.txt'
    small_file='small.txt'
    mid_file='mid.txt'
    # delete files if they exist
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
            print("current_position",current_position*8/1024/1024,"MB")
            # print_memory_usage()
            # print_buffers(buffer_small, buffer_large, buffer_in)
    
    # write remaining buffers to files
    write_buffer_to_file(buffer_small, open(small_file, 'a'))
    write_buffer_to_file(buffer_large, open(large_file, 'a'))
    
    print("current_position",current_position*8/1024/1024,"MB")

    # store fill mid_buffer from mid_heap
    buffer_mid_out = []
    while mid_heap.getMin() is not None:
        val = mid_heap.popMin()
        print(val)
        buffer_mid_out.append(val)
    
    # write mid buffer to file
    write_buffer_to_file(buffer_mid_out, open('mid.txt', 'a'))



    print_buffers(buffer_small, buffer_large, buffer_in)

    end_time = time.time()
    print_memory_usage()
    print(f"Execution time: {end_time - start_time:.2f} seconds ")
    tracemalloc.stop()



    
