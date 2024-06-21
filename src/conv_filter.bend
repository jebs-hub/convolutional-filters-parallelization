import bend.io
import bend.str

fn read_ppm_header(file: io::File) -> (int, int, int) {
    // Read and verify the magic number (P6)
    magic_number = file.read_line().unwrap()
    if magic_number.trim() != "P6" {
        panic("Invalid PPM file: incorrect magic number")
    }

    // Read the width, height, and max color value
    dimensions = file.read_line().unwrap().split_whitespace()
    width = dimensions[0].to_int().unwrap()
    height = dimensions[1].to_int().unwrap()

    max_val = file.read_line().unwrap().to_int().unwrap()

    return (width, height, max_val)
}

fn main() {
    // Open the PPM file
    file_result = io::File::open("images/ppms/star_field.ppm")
    if file_result.is_err() {
        println("Failed to open the file.")
        return
    }
    file = file_result.unwrap()

    // Read the PPM header
    (width, height, max_val) = read_ppm_header(file)

    // Print the image dimensions and max color value
    println("Width: ", width, ", Height: ", height, ", Max Color Value: ", max_val)

    // Read the image data (assuming 3 bytes per pixel in binary format)
    data_result = file.read_bytes(width * height * 3)
    if data_result.is_err() {
        println("Failed to read the image data.")
        return
    }
    data = data_result.unwrap()

    // Process the image data if needed
    // For example, you can convert it to a different format or analyze pixel values

    // Close the file
    file.close()
}
