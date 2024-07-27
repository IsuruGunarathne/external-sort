import random

def create_file():
    target_size = 256 * 1024 * 1024  # 256 MB in bytes
    avg_line_size = 8  # Average size of each line (number + newline)
    num_lines = target_size // avg_line_size
    
    with open('unsorted.txt', 'w') as file:
        for i in range(num_lines):
            file.write(str(random.randint(1, 1000000)) + '\n')
            
    # Ensure the file is exactly 256 MB
    with open('unsorted.txt', 'a') as file:
        while file.tell() < target_size:
            file.write('1\n')

create_file()
print('File created successfully!')
