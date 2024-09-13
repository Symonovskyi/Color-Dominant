import logging
import os
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
from matplotlib.colors import rgb2hex
import matplotlib.pyplot as plt
from collections import defaultdict

# Supported image formats
SUPPORTED_FORMATS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

# Cache for extracted colors to improve performance
color_cache = {}

def extract_colors(image_path, num_colors=5, display_palette=False):
    """
    Extracts dominant colors from an image and optionally displays them in a color palette.

    :param image_path: Path to the image
    :param num_colors: Number of dominant colors to extract (default is 5)
    :param display_palette: Whether to display the color palette (default is False)
    :return: List of dominant colors in HEX format
    """
    try:
        # Check if the image path exists
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file '{image_path}' not found.")
        
        # Return cached result if available
        if image_path in color_cache:
            logging.info(f"Returning cached result for image: {image_path}")
            return color_cache[image_path]

        # Open the image
        img = Image.open(image_path)
        logging.debug(f"Image successfully loaded: {image_path}")

        # Convert the image to a numpy array of pixels
        pixels = np.array(img.convert("RGB"), dtype=np.float32).reshape(-1, 3)
        logging.debug(f"Image converted to pixel array with shape: {pixels.shape}")

        # Normalize pixel values for clustering
        pixels_normalized = pixels / 255.0

        # Perform KMeans clustering
        kmeans = KMeans(n_clusters=num_colors)
        kmeans.fit(pixels_normalized)
        dominant_colors = kmeans.cluster_centers_
        logging.debug(f"Dominant colors found: {dominant_colors}")

        # Convert dominant colors to HEX format
        dominant_colors_hex = [rgb2hex(color) for color in dominant_colors]
        logging.debug(f"Dominant colors in HEX: {dominant_colors_hex}")

        # Cache the result for future use
        color_cache[image_path] = dominant_colors_hex

        # Display color palette if required
        if display_palette:
            display_color_palette(dominant_colors_hex)

        return dominant_colors_hex

    except FileNotFoundError as fnf_error:
        logging.error(fnf_error)
        return []
    except Exception as e:
        logging.error(f"Error while extracting colors: {str(e)}")
        return []

def display_color_palette(dominant_colors):
    """
    Displays a palette of dominant colors.

    :param dominant_colors: List of dominant colors in HEX format
    """
    logging.debug(f"Displaying color palette: {dominant_colors}")
    fig, ax = plt.subplots(1, len(dominant_colors), figsize=(12, 2))
    for i, color in enumerate(dominant_colors):
        ax[i].imshow([[color]])
        ax[i].axis('off')
    plt.show()

def format_colors(colors):
    """
    Formats the list of dominant colors for pleasant output.
    
    :param colors: List of colors in HEX format
    :return: Formatted string representation of colors
    """
    formatted = "\n".join([f"Color {i+1}: {color}" for i, color in enumerate(colors)])
    return f"Dominant colors extracted:\n{formatted}"

def analyze_directory(directory, num_colors=5, display_palette=False, aggregate=False):
    """
    Analyzes all images in the given directory and returns dominant colors.
    
    :param directory: Path to the directory containing images
    :param num_colors: Number of dominant colors to extract
    :param display_palette: Whether to display the palette for each image
    :param aggregate: If True, calculates average dominant colors for all images combined
    :return: A dictionary with filenames as keys and dominant colors as values, or aggregated result
    """
    results = {}
    aggregate_colors = defaultdict(lambda: np.zeros(3))  # For accumulating color sums
    image_count = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(SUPPORTED_FORMATS):
                image_path = os.path.join(root, file)
                logging.info(f"Analyzing image: {image_path}")
                colors = extract_colors(image_path, num_colors, display_palette)
                
                if colors:
                    results[file] = colors
                    if aggregate:
                        # Accumulate color sums for aggregation
                        for i, color in enumerate(colors):
                            aggregate_colors[i] += np.array([int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)])
                        image_count += 1

    if aggregate and image_count > 0:
        # Average the accumulated color sums
        aggregated_result = [
            rgb2hex(aggregate_colors[i] / image_count / 255.0) for i in range(num_colors)
        ]
        return aggregated_result
    return results

def main(image_paths=None, directory=None, num_colors=5, display_palette=False, aggregate=False, log_level=logging.DEBUG):
    # Analyze a group of images either from a list or a directory
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    if image_paths:
        for image_path in image_paths:
            colors = extract_colors(image_path, num_colors, display_palette)
            if colors:
                print(f"Image: {image_path}\n{format_colors(colors)}")
    
    elif directory:
        result = analyze_directory(directory, num_colors, display_palette, aggregate)
        
        if aggregate:
            print(f"Aggregated dominant colors for all images:\n{format_colors(result)}")
        else:
            for image, colors in result.items():
                print(f"Image: {image}\n{format_colors(colors)}")

# If the script is run directly, not imported as a module
if __name__ == "__main__":
    # Setup logging for debugging (this applies to the entire script)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Example 1: Analyze a single image file
    single_image_path = "test_images_directory/test_image1.png"  # Replace with actual image path
    print("Example 1: Analyzing a single image:")
    main(image_paths=[single_image_path])

    # Example 2: Analyze two image files
    image_paths = ["test_images_directory/test_image1.png", "test_images_directory/test_image2.tiff"]  # Replace with actual image paths
    print("\nExample 2: Analyzing two images:")
    main(image_paths=image_paths)

    # Example 3: Analyze all images in a directory with separate results for each image
    directory_path = "test_images_directory"  # Replace with actual directory path
    print("\nExample 3: Analyzing all images in a directory (separate results):")
    main(directory=directory_path)

    # Example 4: Analyze all images in a directory with aggregated result for all images
    print("\nExample 4: Analyzing all images in a directory (aggregated result):")
    main(directory=directory_path, aggregate=True)


