import os
from PIL import Image


def yolo_str_to_bbox(yolo_str, imH, imW):
    # Hàm chuyển từ tọa độ YOLO về (x_min, y_min, x_max, y_max)
    obj_class, x_center, y_center, width, height = map(float, yolo_str.split())
    x_min = int((x_center - width / 2) * imW)
    y_min = int((y_center - height / 2) * imH)
    x_max = int((x_center + width / 2) * imW)
    y_max = int((y_center + height / 2) * imH)
    return obj_class, x_min, y_min, x_max, y_max


def crop_image(image_path, yolo_str):
    # Mở ảnh và lấy kích thước ảnh
    img = Image.open(image_path)
    imW, imH = img.size

    # Lấy tọa độ crop từ YOLO
    _, x_min, y_min, x_max, y_max = yolo_str_to_bbox(yolo_str, imH, imW)

    # Crop ảnh
    cropped_img = img.crop((x_min, y_min, x_max, y_max))
    return cropped_img


def update_labels(label_path, x_min_crop, y_min_crop, new_imW, new_imH):
    # Cập nhật file nhãn dựa trên ảnh đã crop
    new_labels = []
    with open(label_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            obj_class, x_center, y_center, width, height = map(float, line.split())

            # Tính tọa độ mới theo ảnh đã crop
            new_x_center = (x_center * new_imW - x_min_crop) / new_imW
            new_y_center = (y_center * new_imH - y_min_crop) / new_imH
            new_labels.append(
                f"{obj_class} {new_x_center} {new_y_center} {width} {height}"
            )

    # Ghi lại nhãn mới vào file
    with open(label_path, "w") as file:
        file.write("\n".join(new_labels))


def process_directory(root_dir, yolo_str):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".jpg"):
                image_path = os.path.join(subdir, file)
                label_path = os.path.join(subdir, file.replace(".jpg", ".txt"))

                # Crop ảnh
                cropped_img = crop_image(image_path, yolo_str)

                # Lưu ảnh đã crop
                cropped_img.save(image_path)

                # Cập nhật file nhãn của ảnh vừa crop
                x_min_crop, y_min_crop, _, _ = yolo_str_to_bbox(
                    yolo_str, cropped_img.size[1], cropped_img.size[0]
                )
                update_labels(
                    label_path,
                    x_min_crop,
                    y_min_crop,
                    cropped_img.size[0],
                    cropped_img.size[1],
                )

if __name__ == "__main__":
    # Ví dụ sử dụng
    root_dir = "/path/to/your/directory"
    yolo_str = "0 0.5 0.5 0.2 0.2"  # Tọa độ YOLO được cung cấp
    process_directory(root_dir, yolo_str)
