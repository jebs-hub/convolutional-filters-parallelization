def convert_ascii_ppm_to_binary(input_file, output_file):
    with open(input_file, 'r') as f:
        # Read the header
        header = []
        for _ in range(3):
            line = f.readline()
            while line.startswith('#'):  # Skip comments
                line = f.readline()
            header.append(line.strip())
        
        # Parse the header
        format = header[0]
        if format != 'P3':
            raise ValueError("Input file is not an ASCII PPM (P3) image")
        
        width, height = map(int, header[1].split())
        max_val = int(header[2])

        # Read the pixel data
        pixel_data = []
        for line in f:
            if not line.startswith('#'):  # Skip comments
                pixel_data.extend(map(int, line.split()))

    # Write the binary PPM
    with open(output_file, 'wb') as f:
        f.write(b'P6\n')
        f.write(f'{width} {height}\n'.encode())
        f.write(f'{max_val}\n'.encode())
        
        # Convert the pixel data to binary format
        binary_data = bytearray(pixel_data)
        f.write(binary_data)

# Usage example:
input_file = 'images/star_field.ascii.ppm'
output_file = 'images/star_field.ppm'

convert_ascii_ppm_to_binary(input_file, output_file)
