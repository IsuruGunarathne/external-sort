def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

RAM = 16  # 16 MB
chunk_size = 4  # 4 MB
chunk = []

def split_file():
    with open('unsorted.txt', 'r') as file:
        for line in file:
            chunk.append(int(line))
            if file.tell() % (chunk_size * 1024 * 1024) == 0:
                # chunk.sort()
                with open('chunk' + str(file.tell() // (chunk_size * 1024 * 1024)) + '.txt', 'w') as chunk_file:
                    for number in chunk:
                        chunk_file.write(str(number) + '\n')
                chunk.clear()