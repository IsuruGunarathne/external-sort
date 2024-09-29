is_sorted = True
file_name = 'sorted.txt'
prev=0
current=0

# read first line and store in prev
with open(file_name, 'r') as file:
    prev = int(file.readline())
    print("running...")
    for line in file:
        current = int(line)
        # print(prev, current)
        if prev > current:
            is_sorted = False
            break
        prev = current
        
            
if is_sorted:
    print('The file is sorted')
else:
    print('The file is not sorted')
