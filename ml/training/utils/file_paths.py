import os


def get_paths():
    images = []
    masks = []
    for dir in os.listdir("data"):

        for file_path in os.listdir(f"data/{dir}"):

            file_path = f"data/{dir}/{file_path}"
            if file_path.find("mask") != -1:
                masks.append(file_path)
            else:
                images.append(file_path)

    return images, masks
