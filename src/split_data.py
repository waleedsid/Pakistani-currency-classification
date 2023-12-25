import os
import random
import shutil

def split_data(source, train_dest, test_dest, split_ratio=0.8):
    for denomination_folder in os.listdir(source):
        denomination_path = os.path.join(source, denomination_folder)
        images = os.listdir(denomination_path)
        random.shuffle(images)

        split_index = int(len(images) * split_ratio)
        train_images = images[:split_index]
        test_images = images[split_index:]

        for image in train_images:
            src_path = os.path.join(denomination_path, image)
            dest_path = os.path.join(train_dest, denomination_folder, image)

            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            shutil.copy(src_path, dest_path)

        for image in test_images:
            src_path = os.path.join(denomination_path, image)
            dest_path = os.path.join(test_dest, denomination_folder, image)

            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            shutil.copy(src_path, dest_path)

if __name__ == "__main__":
    source_folder = r"D:\Comsis\courses\ai\Pakistani-currency-classification\data-rescaled"
    train_destination = r"D:\Comsis\courses\ai\Pakistani-currency-classification\data\train"
    test_destination = r"D:\Comsis\courses\ai\Pakistani-currency-classification\data\test"

    split_data(source_folder, train_destination, test_destination)
