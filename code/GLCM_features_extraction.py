### Leonardo Politi
### Master degree in Bioinformatics, University of Bologna

# Extracts texture features from brain tumor images using Gray-Level Co-occurrence Matrices (GLCM) and
# saves them into a CSV file. It calculates both first-order (mean, standard deviation, skewness, kurtosis)
# and second-order (entropy, contrast, energy, ASM, homogeneity, dissimilarity, correlation) features.
# The images are categorized into four classes (glioma, meningioma, pituitary, healthy) based on their filenames.

import os
from PIL import Image
import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis
from skimage.feature import graycomatrix, graycoprops

def extract_texture_features(img, distances = [1], angles = [np.pi/2], levels= 256):
    img_array = np.array(img.convert('L'))
    glcm = graycomatrix(img_array, distances=distances, angles=angles, levels=levels, normed=True, symmetric= True)
    features = {}

    # First order features
    features['mean'] = np.mean(img_array)
    #features['variance'] = np.var(img_array)
    features['std'] = np.std(img_array)
    features['skewness'] = skew(img_array.ravel())
    features['kurtosis'] = kurtosis(img_array.ravel())

    # Second order features (mean over different angles)
    glcm_marginal = np.sum(glcm, axis=1)
    entropy = -np.sum(glcm_marginal * np.log2(glcm_marginal + 1e-15))  # Add small value to avoid log(0)
    features['entropy'] = entropy
    features['contrast'] = np.mean(graycoprops(glcm, 'contrast'))
    features['energy'] = np.mean(graycoprops(glcm, 'energy'))
    features['ASM'] = np.mean(graycoprops(glcm, 'ASM'))
    features['homogeneity'] = np.mean(graycoprops(glcm, 'homogeneity'))
    features['dissimilarity'] = np.mean(graycoprops(glcm, 'dissimilarity'))
    features['correlation'] = np.mean(graycoprops(glcm, 'correlation'))

    return features

#---------------------------------
if __name__ == '__main__':
    data_dir = 'brain_tumor_data'

    all_features = []
    for root, dirs, files in os.walk(data_dir):
        for filename in files:
            image_path = os.path.join(root, filename)

            # Determines class based on subdirectory
            if 'glioma' in root.lower():
                class_label = 1
            elif 'meningioma' in root.lower():
                class_label = 2
            elif 'pituitary' in root.lower():
                class_label = 3
            elif 'notumor' in root.lower():
                class_label = 0
            else:
                print('Error: Unexpected subdirectory', root)
                continue

            try:
                with Image.open(image_path) as img:
                    features = extract_texture_features(img)
                    features['image_name'] = filename
                    features['class'] = class_label
                    all_features.append(features)

            except (IOError, OSError) as e:
                print(f"Error processing {filename}: {e}")

    data = pd.DataFrame(all_features)
    print('Dataframe dimensions:', data.shape)
    print(data)

    # Save data as csv
    data.to_csv('brain_tumor_texture.csv')

