from PIL import Image
import os


def overlay_images(
    base_image_path, overlay_image_path, output_image_path, x_offset, y_offset
):
    # Open the two images
    base_image = Image.open(base_image_path)
    overlay_image = Image.open(overlay_image_path)
    width, height = overlay_image.size
    new_width = int(width * 0.8)
    new_height = int(height * 0.8)
    scaled_image = overlay_image.resize((new_width, new_height), Image.LANCZOS)
    # Calculate the position to place the overlay image
    x_position = x_offset
    y_position = y_offset

    # Create a new image with the size of the base image
    result_image = Image.new("RGBA", base_image.size)

    # Paste the base image onto the new image
    result_image.paste(base_image, (0, 0))

    # Paste the overlay image onto the new image at the specified position
    result_image.paste(scaled_image, (x_position, y_position), mask=scaled_image)

    # Save the resulting image to the specified output path
    result_image.save(output_image_path)


# Example usage:
def cut8(input_string):
    result_string = input_string[7:]
    return result_string


def process_files_in_directory(directory_path):
    # Get a list of filenames in the directory
    filenames = os.listdir(directory_path)

    # Loop through the filenames
    for filename in filenames:
        # Create the absolute path of the file
        file_path = os.path.join(directory_path, filename)

        # Check if the file is a regular file (not a directory)
        if os.path.isfile(file_path):
            base_image_path = "Front.png"  # Replace with the path to your base image
            overlay_image_path = (
                file_path  # Replace with the path to your overlay image
            )
            new_path = cut8(file_path)
            output_image_path = (
                f"white_pieces/{new_path}"  # Replace with the desired output path
            )
            x_offset = 60  # Adjust the x offset based on your requirement
            y_offset = 80  # Adjust the y offset based on your requirement
            overlay_images(
                base_image_path,
                overlay_image_path,
                output_image_path,
                x_offset,
                y_offset,
            )


# Example usage:
directory_path = "Regular"  # Replace with the directory path

process_files_in_directory(directory_path)
