### Leonardo Politi
### Master degree in Bioinformatics, University of Bologna

# Removes duplicate images based on MD5 hashes and provides an option to rename files
# in a structured format for better organization.

import hashlib
import os

def compute_hash(file):
    hasher = hashlib.md5()
    with open(file, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

#-------

def list_files(data_dir, rename = False):
    hash_dict = {}
    counter = 1
    for subdir in os.listdir(data_dir):
        counter = 1
        if os.path.isdir(os.path.join(data_dir, subdir)):
            for root, dirs, files in os.walk(os.path.join(data_dir, subdir)):
                for file in files:
                    if file.endswith(".jpg"):
                        file_path = os.path.join(root, file)
                        if rename:
                            new_file_name = f"{subdir}_{counter:03d}.jpg"
                            new_file_path = os.path.join(root, new_file_name)
                            os.rename(file_path, new_file_path)
                            file_path = new_file_path
                            counter += 1

                        file_hash = compute_hash(file_path)

                        if file_hash not in hash_dict:
                            hash_dict[file_hash] = []
                        hash_dict[file_hash].append(file_path)
                    else: print(file, 'is not .jpg!')

    return hash_dict

#----------

def remove_duplicates(hash_dict):
    duplicate_count = 0
    for hash_value, file_paths in hash_dict.items():
        if len(file_paths) > 1:
            for file_path in file_paths[1:]:
                print(f"Removing duplicate (hash : {hash_value}) : {file_path}")
                os.remove(file_path)
                duplicate_count += 1
    print(f"Number of duplicates removed : {duplicate_count}")

#####################################################################################

if __name__ == '__main__':
    data_dir = 'brain_tumor_data_raw'
    hash_dict = list_files(data_dir, rename = True)  # Also rename files
    print(hash_dict)
    remove_duplicates(hash_dict)
