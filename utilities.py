"""
This module provides utility functions for loading, processing, and visualizing depth data from binary files.

Functions:
- load_input_file_paths: Loads the file paths of input data files from a specified directory.
- load_depth_data_sets: Loads depth data sets from a list of binary files.
- load_depth_data_frames: Loads depth data frames from a binary file.
- create_gif_from_frames: Creates a GIF from a sequence of frames and saves it to a specified file.
- get_absolute_path_and_mkdirs: Ensures the directory for a given file path exists and returns the absolute path.

Constants:
- DEFAULT_FRAME_WIDTH: The default width of each frame.
- DEFAULT_FRAME_HEIGHT: The default height of each frame.
- DATA_DIR_NAME: The name of the directory containing the input data files.

Dependencies:
- os: Provides a way of using operating system dependent functionality.
- numpy: A package for scientific computing with Python.
- matplotlib.pyplot: A plotting library for creating static, animated, and interactive visualizations.
- PIL: Python Imaging Library, adds image processing capabilities.
- typing: Provides runtime support for type hints.
"""

import os
import uuid
import numpy as np
import matplotlib.pyplot as plt

from typing import List


DEFAULT_FRAME_WIDTH = 80
DEFAULT_FRAME_HEIGHT = 60
INPUT_FOLDER = "input"
OUTPUT_FOLDER = "output"


def load_input_file_paths(input_data_dir: str = INPUT_FOLDER) -> List[str]:
    """
    Loads the file paths of input data files from the specified directory.

    This function searches for files with a ".bin" extension in the given directory.
    If the directory does not exist or is empty, the function will print an error message and exit.
    If a file does not exist or does not have the correct file type, it will be skipped.

    Args:
        input_data_dir (str): The directory to search for input data files. Defaults to DATA_DIR_NAME.

    Returns:
        List[str]: A list of absolute file paths to the input data files.

    Raises:
        SystemExit: If the directory does not exist or is empty.
    """
    if os.path.isabs(input_data_dir):
        data_abs_path = os.path.join(os.path.dirname(__file__), input_data_dir)
    else:
        data_abs_path = input_data_dir

    if not os.path.exists(data_abs_path):
        print(f"Directory {data_abs_path} does not exist")
        exit(1)

    file_names = []

    for file_name in os.listdir(data_abs_path):
        abs_file_path = os.path.join(data_abs_path, file_name)

        if not os.path.isfile(abs_file_path):
            print(f"Could not load file {abs_file_path} because it does not exist")
            continue

        if not os.path.splitext(file_name)[1] == ".bin":
            print(
                f"Skipping file {file_name} because it doesn't have the correct file type"
            )
            continue

        file_names.append(abs_file_path)

    if not len(file_names):
        print(f"Input directory {data_abs_path} is empty")
        exit(1)

    return file_names


def load_depth_data_sets(
    file_names: List[str],
    width: int = DEFAULT_FRAME_WIDTH,
    height: int = DEFAULT_FRAME_HEIGHT,
) -> dict[np.ndarray]:
    """
    Loads depth data sets from a list of binary files.

    This function reads binary files containing depth data and converts them into a dictionary of numpy arrays.
    Each key in the dictionary is the file name (with spaces replaced by underscores and the extension changed to ".gif"),
    and the corresponding value is a numpy array containing the depth data frames.

    Args:
        file_names (List[str]): A list of file paths to the binary files.
        width (int, optional): The width of each frame. Defaults to DEFAULT_FRAME_WIDTH.
        height (int, optional): The height of each frame. Defaults to DEFAULT_FRAME_HEIGHT.
    Returns:
        dict[np.ndarray]: A dictionary where the keys are file names and the values are numpy arrays of depth data frames.
    """
    data_sets = {}

    for file_name in file_names:
        try:
            data_sets[file_name] = load_depth_data_frames(file_name, width, height)
        except ValueError as e:
            print(f"{file_name}: {e}")
            continue

    return data_sets


def load_depth_data_frames(
    file_name: str, width: int = DEFAULT_FRAME_WIDTH, height: int = DEFAULT_FRAME_HEIGHT
) -> np.ndarray:
    """
    Loads depth data frames from a binary file.
    This function reads depth data from a binary file and reshapes it into a 3D numpy array
    with the specified width and height for each frame. The data is expected to be in
    float64 format.
    Args:
        file_name (str): The path to the binary file containing the depth data.
        width (int, optional): The width of each frame. Defaults to DEFAULT_FRAME_WIDTH.
        height (int, optional): The height of each frame. Defaults to DEFAULT_FRAME_HEIGHT.
    Returns:
        np.ndarray: A 3D numpy array of shape (num_frames, height, width) containing the
        depth data frames. If the file is not found, an empty array is returned.
    Raises:
        ValueError: If the total size of the data is not divisible by the product of width
        and height, indicating an incorrect frame size.
    """
    try:
        with open(file_name, "rb") as file:
            data = np.fromfile(file, dtype=np.float64)
    except FileNotFoundError as e:
        print(e)
        return np.array([])

    if data.size % (width * height) != 0:
        raise ValueError(f"Incorrect frame size {width} x {height}")

    return data.reshape(-1, height, width)


def create_heatmap(
    data_array: np.ndarray,
    data_set_path: str,
    cmap: str = "viridis",
    dpi: int = 100,
):
    """
    Generate heatmap images for each frame in the provided 3D numpy arrays.

    Parameters:
        data_array (np.ndarray): 3D array containing the sample data (shape: [num_frames, height, width]).
        output_dir (str): Directory to save heatmap images.
        cmap (str): Matplotlib colormap to use.
        dpi (int): DPI for output images.
    """
    file_name_with_ext = data_set_path.split(os.path.sep)[-1]
    file_name, _ = os.path.splitext(file_name_with_ext)

    output_dir = os.path.join(OUTPUT_FOLDER, file_name)
    os.makedirs(output_dir, exist_ok=True)

    data_set_uuid = uuid.uuid4()

    num_frames = data_array.shape[0]

    for frame_no in range(num_frames):
        frame = data_array[frame_no, :, :]

        fig, ax = plt.subplots(
            figsize=(DEFAULT_FRAME_WIDTH / 10, DEFAULT_FRAME_HEIGHT / 10)
        )
        im = ax.imshow(frame, cmap=cmap, interpolation="nearest")

        ax.axis("off")
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        filename = os.path.join(output_dir, f"{data_set_uuid}_frame_{frame_no:04d}.png")
        plt.savefig(filename, dpi=dpi, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
