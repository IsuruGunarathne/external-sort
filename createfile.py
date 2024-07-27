import random

def create_file():
    size = 256
    target_size = size * 1024 * 1024  # 256 MB in bytes
    avg_line_size = 8  # Average size of each line (number + newline)
    num_lines = target_size // avg_line_size
    additional_lines = 0

    print('Creating file ' + str(size) + ' MB...')
    print('Number of lines: ' + str(num_lines))
    
    with open('unsorted.txt', 'w') as file:
        for i in range(num_lines):
            file.write(str(random.randint(1, 1000000)) + '\n')
            
    # Ensure the file is 256 MB
    with open('unsorted.txt', 'a') as file:
        while file.tell() < target_size:
            file.write(str(random.randint(1, 1000000)) + '\n')
            additional_lines += 1
    
    print('Additional lines added: ' + str(additional_lines))
    approximation_error = (additional_lines / num_lines) * 100
    print('Approximation error: ' + str(round(approximation_error, 3)) + '%')
        
create_file()
print('File created successfully!')
