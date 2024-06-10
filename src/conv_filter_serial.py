import sys
import numpy as np
from scipy.ndimage import convolve

def read_ppm(filename):
    with open(filename, 'rb') as f:
        header = f.readline().decode('ascii').strip()
        if header != 'P6':
            raise ValueError("Unsupported PPM format: must be 'P6'")

        dimensions = f.readline().decode('ascii').strip()
        while dimensions.startswith('#'):
            dimensions = f.readline().decode('ascii').strip()

        width, height = map(int, dimensions.split())
        max_val = int(f.readline().decode('ascii').strip())
        pixel_data = np.frombuffer(f.read(), dtype=np.uint8)
        pixel_data = pixel_data.reshape((height, width, 3))

        return pixel_data, width, height, max_val

def write_ppm(filename, data, width, height, max_val):
    with open(filename, 'wb') as f:
        f.write(b'P6\n')
        f.write(f'{width} {height}\n'.encode())
        f.write(f'{max_val}\n'.encode())
        f.write(data.tobytes())

def apply_blur_filter(image, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size)) / (kernel_size ** 2)
    blurred_image = np.zeros_like(image)

    for channel in range(3):
        blurred_image[..., channel] = convolve(image[..., channel], kernel, mode='reflect')

    return blurred_image

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    image, width, height, max_val = read_ppm(input_file)
    blurred_image = apply_blur_filter(image)
    write_ppm(output_file, blurred_image, width, height, max_val)

    print(f'Blurred image saved as {output_file}')
