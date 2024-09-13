# Color Dominant

## Description

**Color Dominant** is a Python module designed to automatically extract dominant colors from images. It supports single or batch image analysis, allowing you to process individual files or entire directories. The tool provides both separate results for each image or an aggregated result for all images.

<img src="https://raw.githubusercontent.com/Symonovskyi/Symonovskyi/main/src/projects/Color-Dominant/Color-Dominant-background.webp" alt="background">

## Features

Key features include:

- **Single Image Analysis**: Extracts dominant colors from a single image.
- **Multiple Image Analysis**: Processes several image files at once.
- **Directory Analysis**: Automatically scans a folder and analyzes all supported images within it.
- **Result Aggregation**: Option to combine results for all images into a single aggregated result.
- **Popular Formats Supported**: PNG, JPEG, BMP, TIFF, and others.
- **Flexible Logging**: Provides detailed logging to assist in debugging and monitoring processes.

### Parameters

The `main` function and command-line interface accept the following parameters:

- **image_paths**: List of image file paths to analyze. Example: `["image1.png", "image2.jpg"]`
- **directory**: Path to a directory containing images to analyze. Example: `"./images_folder"`
- **num_colors**: Number of dominant colors to extract per image (default: 5). Example: `5`
- **display_palette**: Whether to display a color palette of dominant colors (default: `False`). Example: `True`
- **aggregate**: Whether to aggregate the results across all images (default: `False`). Example: `True`
- **log_level**: The logging level (default: `DEBUG`). Can be one of `DEBUG`, `INFO`, `WARNING`, `ERROR`. Example: `INFO`

---

### Installation

To get started, clone the repository and install dependencies:

1. Clone the repository:

    ```bash
    git clone https://github.com/Symonovskyi/Color-Dominant.git
    cd Color-Dominant
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

---

### Usage Examples

#### Command-Line Interface

##### Simple Example (Single File)

Analyze a single image file and extract dominant colors:

```bash
python color_dominant.py --image_paths path_to_your_image.png
```

##### Advanced Example (Multiple Parameters)

Analyze all images in a directory, display a palette, and aggregate the results:

```bash
python color_dominant.py --directory path_to_your_directory --num_colors 7 --display_palette --aggregate
```

#### Module Usage

##### Simple Example (Single File)

```python
from color_dominant import main

# Analyze a single image
image_path = "path_to_your_image.png"
main(image_paths=[image_path])
```

##### Advanced Example (All Parameters)

```python
from color_dominant import main

# Analyze images from a directory, display palettes, and aggregate results
directory_path = "path_to_your_directory"
main(directory=directory_path, num_colors=7, display_palette=True, aggregate=True, log_level="INFO")
```

---

## Licensing

This project is distributed under a dual license: [MIT License](./LICENSE_MIT) and [Creative Commons Attribution 4.0 International (CC BY 4.0)](./LICENSE_CC_BY_4.0).

### What does this mean for you?

When you use this project, we just ask that you follow a few simple rules:

1. **Give Credit**: Please make sure to give proper credit to the authors of this project. This can be as simple as including a notice in your documentation or about page, linking back to the original project.
2. **Share Any Changes**: If you make any modifications, let others know by mentioning that changes were made. This helps keep things transparent and benefits the community.
3. **Keep These Licenses with the Project**: When you share or distribute this project, just make sure that both license files stay with it. That’s all! This ensures that everyone knows the rules, just like you do.

We’re excited to see what you create with this project! Thank you for following these simple guidelines and helping keep the spirit of open source alive and well.















