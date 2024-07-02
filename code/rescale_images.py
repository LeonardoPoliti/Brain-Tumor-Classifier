### Leonardo Politi
### Master degree in Bioinformatics, University of Bologna

# Extracts image metadata (dimensions, aspect ratio), visualizes image characteristics, resizes and crops
# images to a standardized format and convert all images into grayscale.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import imagesize
import os
import shutil


def get_image_metadata(data_dir):
    """Collects metadata (filename, size, aspect ratio) for images in a directory and its subfolders."""
    all_img_meta = []
    for class_name in os.listdir(data_dir):
        class_dir = os.path.join(data_dir, class_name)
        if os.path.isdir(class_dir):  # Make sure it's a directory
            for filename in os.listdir(class_dir):
                if filename.endswith(".jpg"):
                    img_path = os.path.join(class_dir, filename)
                    width, height = imagesize.get(img_path)
                    aspect_ratio = round(width / height, 2)
                    all_img_meta.append({
                        'Class': class_name,
                        'FileName': filename,
                        'Width': width,
                        'Height': height,
                        'Aspect_Ratio': aspect_ratio
                    })
    return pd.DataFrame(all_img_meta)

def resize_and_crop_images(data_dir, target_size=(256, 256), grayscale = True):
    """Resizes and crops images in a directory to a target size, ensuring 1:1 aspect ratio."""
    for subdir in os.listdir(data_dir):
        if os.path.isdir(os.path.join(data_dir, subdir)):
            for root, dirs, files in os.walk(os.path.join(data_dir, subdir)):
                for file in files:
                    if file.endswith(".jpg"):
                        file_path = os.path.join(root, file)
                        try:
                            with Image.open(file_path) as img:
                                if grayscale:
                                    img = img.convert('L')  # convert into gray scale
                                width, height = img.size
                                if width != height:
                                    # cropping dimensions
                                    if width > height:
                                        left = (width - height) // 2
                                        top = 0
                                        right = left + height
                                        bottom = height
                                    else:
                                        left = 0
                                        top = (height - width) // 2
                                        right = width
                                        bottom = top + width

                                    img = img.crop((left, top, right, bottom))

                                img_resized = img.resize(target_size, Image.LANCZOS)
                                img_resized.save(file_path)

                        except (IOError, OSError) as e:
                            print(f"Error processing {file_path}: {e}")


def move_files_to_parent(main_folder):
    """Moves files from subfolders to the parent directory and removes empty subfolders."""
    for item in os.listdir(main_folder):
        item_path = os.path.join(main_folder, item)
        if os.path.isdir(item_path):  # check if it's a subfolder
            for file_name in os.listdir(item_path):
                file_path = os.path.join(item_path, file_name)
                shutil.move(file_path, main_folder)
            os.rmdir(item_path)
            print(f"Removed subfolder: {item}")


##############################################################################

if __name__ == '__main__':
    remove_subdir = False  # if 'True' move all images in the same directory
    data_dir = 'brain_tumor_data_raw'
    img_meta_df = get_image_metadata(data_dir)

    # Scatter Image Resolutions - before scaling
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    points = ax.scatter(img_meta_df.Width, img_meta_df.Height,  color='blue', alpha=0.5, s=10, picker=True)
    ax.set_title("Image Resolution - Before scaling")
    ax.set_xlabel("Width", size=14)
    ax.set_ylabel("Height", size=14)
    plt.show()

    # Aspect Ratio Distribution - before cropping
    grid = sns.FacetGrid(img_meta_df, col='Class', col_wrap=2)
    grid.map(plt.hist, 'Aspect_Ratio', bins=20, edgecolor='k', alpha=0.7)
    grid.set_axis_labels('Aspect Ratio', 'Number of Images')
    grid.fig.suptitle('Image Aspect Ratio Distribution - before cropping')
    plt.subplots_adjust(top=0.9)  # Adjust title position to avoid overlap
    plt.show()

    print('Aspect Ratio Count:', '\n', img_meta_df.groupby(['Aspect_Ratio'])['Class'].count())

    ###  Resize and crop images
    resize_and_crop_images(data_dir, target_size=(256, 256), grayscale=True)  # also make sure that all images have only 1 channel
    img_meta_df = get_image_metadata(data_dir)

    # Aspect Ratio Distribution - after cropping
    plt.figure(figsize=(8, 6))
    plt.hist(img_meta_df['Aspect_Ratio'], bins=20, edgecolor='k', alpha=0.7)
    plt.xlabel('Aspect Ratio')
    plt.ylabel('Number of Images')
    plt.title('Image Aspect Ratio Distribution (all classes) - after cropping')
    plt.show()

    ### Remove subdirectoris and move all images into the parent folder.
    if remove_subdir:
        move_files_to_parent(data_dir)

    ### Rename main image folder
    os.rename(data_dir, 'brain_tumor_data')




