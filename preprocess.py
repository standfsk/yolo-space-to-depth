import os
from PIL import Image
from tqdm import tqdm
from pathlib import Path
import zipfile


def convert_box(size, box):
    # Convert VisDrone box to YOLO xywh box
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    return (box[0] + box[2] / 2) * dw, (box[1] + box[3] / 2) * dh, box[2] * dw, box[3] * dh

def visdrone2yolo(pth, name):
    os.makedirs(pth / "images", exist_ok=True)
    os.makedirs(pth / "labels", exist_ok=True)
    zip_file = zipfile.ZipFile(name + ".zip", "r")
    image_files = [file_name for file_name in zip_file.namelist() if file_name.endswith(".jpg")]
    for image_file_name in tqdm(image_files, desc=f"processing {name}.zip"):
        image_file = zip_file.open(image_file_name)
        image = Image.open(image_file)
        image_size = image.size
        image.save(pth / "images" / os.path.basename(image_file_name))
        image_file.close()

        label_file_name = image_file_name.replace(f"images", f"annotations").replace(".jpg", ".txt")
        label_file = zip_file.open(label_file_name, "r")
        label_data = label_file.read().strip().decode("utf-8").splitlines()
        lines = []
        for row in [x.split(",") for x in label_data]:
            if row[4] == "0":
                continue
            cls = int(row[5]) - 1
            box = convert_box(image_size, tuple(map(int, row[:4])))
            lines.append(f"{cls} {' '.join(f'{x:.6f}' for x in box)}\n")

            with open(pth / "labels" / os.path.basename(label_file_name), "w") as label_save_file:
                label_save_file.writelines(lines)
        label_file.close()
    zip_file.close()

if __name__ == "__main__":
    dpath = Path("dataset/VisDrone")

    for mode, name in ["train", "VisDrone2019-DET-train"], ["val", "VisDrone2019-DET-val"], ["test", "VisDrone2019-DET-test-dev"]:
        visdrone2yolo(dpath / mode, name)
