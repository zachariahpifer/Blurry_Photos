import cv2
import os
import config
from shutil import copyfile

# Folder to be analyzed 
global path
path = "D:\Pic dump\Test"

def create_folders():
    # Create folders for copied images.
    folders = ["blurred", "focused"]
    for folder in folders:
        new_path = os.path.join(path, folder)
        try:
            os.makedirs(new_path, exist_ok=True)
            print("Directory '%s' created successfully" %new_path)
        except OSError as error:
            print("Directory '%s' can not be created")


def get_images():
    # Get list of filenames - collect all jpgs, collect RAW without corresponding jpg.
    # Returns list of iamge filenames.
    images =  list(set([f for f in os.listdir(path) if f.endswith('.JPG')]))
    images.sort()
    return images


def create_histogram(image_path):
    # Read image and create histogram.
    img = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([img], config.channels, None, config.histSize, config.ranges, accumulate=False)
    cv2.normalize(hist, hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    return hist


def find_focused(images):
    # Finds most in-focus image by calculating Laplacian variance of (B&W) image.
    # Largest variance is, theoretically, most focused. 
    max_laplacian = 0
    best_image = ""
    for image in images:
        img = cv2.cvtColor(cv2.imread(os.path.join(path,image)), cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
        if laplacian > max_laplacian and laplacian > config.blur_threshold:
            max_laplacian = laplacian
            best_image = image
    return best_image


def main():
    create_folders()
    images = get_images()
    similar_image_count = 0
    i=0
    while i < len(images)-1:
        similar_images = [images[i]]
        base_hist = create_histogram(os.path.join(path,images[i]))
        while i < len(images)-1:
            i+=1
            cmp_hist = create_histogram(os.path.join(path,images[i]))
            correlation = cv2.compareHist(base_hist, cmp_hist, 0)
            if correlation < .75:
                break
            else:
                similar_images.append(images[i])
        best_image = find_focused(similar_images)
        if best_image != "":
            similar_image_count+=1
        for image in similar_images:
            if image == best_image:
                copyfile(os.path.join(path,image), os.path.join(path,"focused",image))
            else:
                copyfile(os.path.join(path,image), os.path.join(path,"blurred",image))

    print("Program completed successfully. Identified ", similar_image_count, " similar images.")


if __name__ == "__main__":
    main()