import sys

def read_ppm(filename):
    with open(filename, 'rb') as f:
        # Read and validate PPM header
        format = f.readline().decode().strip()
        if format != 'P6':
            raise ValueError(f"Invalid PPM format in {filename}. Expected 'P6'.")

        # Read width, height, and max_val
        width, height = map(int, f.readline().decode().strip().split())
        max_val = int(f.readline().decode().strip())

        # Read pixel data
        raw_data = f.read()
    
    # Convert raw data to Pixel array
    pixels = []
    for i in range(width * height):
        r = raw_data[i * 3]
        g = raw_data[i * 3 + 1]
        b = raw_data[i * 3 + 2]
        pixels.append((r, g, b))
    
    return {'width': width, 'height': height, 'max_val': max_val, 'pixels': pixels}

def compare_ppm_files(file1, file2):
    try:
        img1 = read_ppm(file1)
        img2 = read_ppm(file2)

        # Compare image metadata
        if img1['width'] != img2['width'] or img1['height'] != img2['height'] or img1['max_val'] != img2['max_val']:
            return False

        # Compare pixel data
        if img1['pixels'] != img2['pixels']:
            return False

        return True

    except Exception as e:
        print(f"Error comparing PPM files: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compare_ppm.py <file to check>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = "images/1_serial_out.ppm"

    if compare_ppm_files(file1, file2):
        print(f"The files {file1} and {file2} are equal.")
    else:
        print(f"The files {file1} and {file2} are not equal.")

