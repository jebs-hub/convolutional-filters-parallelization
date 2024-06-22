#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

typedef struct {
    unsigned char r, g, b;
} Pixel;

typedef struct {
    int width;
    int height;
    int max_val;
    Pixel *data;
} Image;

Image read_ppm(const char *filename) {
    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        fprintf(stderr, "Unable to open file '%s'\n", filename);
        exit(1);
    }

    char format[3];
    fscanf(fp, "%2s", format);
    if (format[0] != 'P' || format[1] != '6') {
        fprintf(stderr, "Invalid PPM format (must be 'P6')\n");
        exit(1);
    }

    Image img;
    fscanf(fp, "%d %d", &img.width, &img.height);
    fscanf(fp, "%d", &img.max_val);
    fgetc(fp);

    img.data = (Pixel *)malloc(img.width * img.height * sizeof(Pixel));
    fread(img.data, sizeof(Pixel), img.width * img.height, fp);

    fclose(fp);
    return img;
}

void write_ppm(const char *filename, Image *img) {
    FILE *fp = fopen(filename, "wb");
    if (!fp) {
        fprintf(stderr, "Unable to open file '%s'\n", filename);
        exit(1);
    }

    fprintf(fp, "P6\n%d %d\n%d\n", img->width, img->height, img->max_val);
    fwrite(img->data, sizeof(Pixel), img->width * img->height, fp);

    fclose(fp);
}

Pixel apply_kernel(Pixel *data, int width, int height, int x, int y, int kernel_size) {
    int half_size = kernel_size / 2;
    int sum_r = 0, sum_g = 0, sum_b = 0;
    int count = 0;

    for (int ky = -half_size; ky <= half_size; ky++) {
        for (int kx = -half_size; kx <= half_size; kx++) {
            int nx = x + kx;
            int ny = y + ky;

            if (nx >= 0 && nx < width && ny >= 0 && ny < height) {
                Pixel p = data[ny * width + nx];
                sum_r += p.r;
                sum_g += p.g;
                sum_b += p.b;
                count++;
            }
        }
    }

    Pixel result;
    result.r = sum_r / count;
    result.g = sum_g / count;
    result.b = sum_b / count;
    return result;
}

void apply_blur_filter(Image *img, int kernel_size) {
    Pixel *blurred_data = (Pixel *)malloc(img->width * img->height * sizeof(Pixel));

    #pragma omp parallel for collapse(2)
    for (int y = 0; y < img->height; y++) {
        for (int x = 0; x < img->width; x++) {
            blurred_data[y * img->width + x] = apply_kernel(img->data, img->width, img->height, x, y, kernel_size);
        }
    }

    free(img->data);
    img->data = blurred_data;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <input_image> <output_image> <num_threads>\n", argv[0]);
        return 1;
    }

    const char *input_file = argv[1];
    const char *output_file = argv[2];
    int num_threads = atoi(argv[3]);

    if (num_threads <= 0) {
        fprintf(stderr, "Number of threads must be a positive integer\n");
        return 1;
    }

    omp_set_num_threads(num_threads);

    Image img = read_ppm(input_file);
    apply_blur_filter(&img, 3);
    write_ppm(output_file, &img);

    free(img.data);
    printf("Blurred image saved as %s\n", output_file);

    return 0;
}
