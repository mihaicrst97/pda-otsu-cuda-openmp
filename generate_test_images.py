import os
import numpy as np
from PIL import Image

# --- Configuration ---
OUTPUT_DIR = "generated_test_images"
RESOLUTIONS = {
    "small_480p": (640, 480),
    "medium_720p": (1280, 720),
    "large_1080p": (1920, 1080),
    "xlarge_4k": (3840, 2160),
    "xxlarge_8k": (7680, 4320),
    # You can add more resolutions here if you want
    # "custom_1": (100, 100),
    # "custom_2": (1000, 1000),
}

# --- Main Script ---
def main():
    # Create the output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: '{OUTPUT_DIR}'")

    print("Generating test images...")

    for name, (width, height) in RESOLUTIONS.items():
        # Generate a random numpy array with grayscale values (0-255)
        # Using uint8 is important for memory efficiency and PIL compatibility
        random_pixels = np.random.randint(0, 256, (height, width), dtype=np.uint8)

        # Create a Pillow Image from the numpy array
        img = Image.fromarray(random_pixels, mode='L') # 'L' mode is for grayscale

        # Define the output path
        file_path = os.path.join(OUTPUT_DIR, f"{name}_{width}x{height}.png")

        # Save the image
        img.save(file_path)
        print(f"  - Saved {file_path}")

    print("\nImage generation complete.")
    print(f"You can now run the C++ project on the '{OUTPUT_DIR}' folder.")

if __name__ == '__main__':
    main()
