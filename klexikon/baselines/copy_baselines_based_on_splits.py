"""
For baselines with existing predictions for the full dataset, we can simply copy the corresponding validation/test
files into a separate folder to get results without having to re-compute them.
"""

import os
from shutil import copyfile

if __name__ == '__main__':
    base_dir = "./data/baselines_all_articles"

    validation_file_dir = "./data/splits/validation/klexikon"
    test_file_dir = "./data/splits/test/klexikon"

    validation_dir = "./data/baselines_validation"
    test_dir = "./data/baselines_test"

    os.makedirs(validation_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    for potential_dir in os.listdir(base_dir):
        # Exclude non-directory objects
        if not os.path.isdir(os.path.join(base_dir, potential_dir)):
            continue

        os.makedirs(os.path.join(validation_dir, potential_dir), exist_ok=True)
        os.makedirs(os.path.join(test_dir, potential_dir), exist_ok=True)

        for fn in os.listdir(validation_file_dir):
            copyfile(os.path.join(base_dir, potential_dir, fn), os.path.join(validation_dir, potential_dir, fn))

        for fn in os.listdir(test_file_dir):
            copyfile(os.path.join(base_dir, potential_dir, fn), os.path.join(test_dir, potential_dir, fn))




