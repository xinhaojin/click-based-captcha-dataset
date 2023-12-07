import os
import shutil
import xml.etree.ElementTree as ET


class_names = ['word', 'icon']
# voc_dir = '/home/jxh/work/datasets/all'
# yolo_dir = '/home/jxh/work/datasets/all'
voc_dir = '.'
yolo_dir = '.'

# 创建yolo格式的目录结构
os.makedirs(os.path.join(yolo_dir, 'images', 'train'), exist_ok=True)
os.makedirs(os.path.join(yolo_dir, 'images', 'val'), exist_ok=True)
os.makedirs(os.path.join(yolo_dir, 'images', 'test'), exist_ok=True)
os.makedirs(os.path.join(yolo_dir, 'labels', 'train'), exist_ok=True)
os.makedirs(os.path.join(yolo_dir, 'labels', 'val'), exist_ok=True)
os.makedirs(os.path.join(yolo_dir, 'labels', 'test'), exist_ok=True)

# 读取训练集、验证集和测试集的文件名
with open(os.path.join(voc_dir, 'ImageSets', 'Main', 'train.txt')) as f:
    train_list = f.read().splitlines()
with open(os.path.join(voc_dir, 'ImageSets', 'Main', 'val.txt')) as f:
    val_list = f.read().splitlines()
with open(os.path.join(voc_dir, 'ImageSets', 'Main', 'test.txt')) as f:
    test_list = f.read().splitlines()

# 转换标注文件格式
for split_name, split_list in [('train', train_list), ('val', val_list), ('test', test_list)]:
    for image_name in split_list:
        # 复制图片
        src_image_path = os.path.join(voc_dir, 'JPEGImages', f'{image_name}.png')
        dst_image_path = os.path.join(yolo_dir, 'images', split_name, f'{image_name}.jpg')
        shutil.copy(src_image_path, dst_image_path)
        
        # 解析XML标注文件
        xml_path = os.path.join(voc_dir, 'Annotations', f'{image_name}.xml')
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 获取图片大小
        size_elem = root.find('size')
        width = int(size_elem.find('width').text)
        height = int(size_elem.find('height').text)

        # 转换标注
        with open(os.path.join(yolo_dir, 'labels', split_name, f'{image_name}.txt'), 'w') as f:
            for obj_elem in root.findall('object'):
                class_name = obj_elem.find('name').text
                if class_name not in class_names:
                    continue

                bbox_elem = obj_elem.find('bndbox')
                xmin = int(float(bbox_elem.find('xmin').text))
                ymin = int(float(bbox_elem.find('ymin').text))
                xmax = int(float(bbox_elem.find('xmax').text))
                ymax = int(float(bbox_elem.find('ymax').text))

                x_center = (xmin + xmax) / 2 / width
                y_center = (ymin + ymax) / 2 / height
                w = (xmax - xmin) / width
                h = (ymax - ymin) / height

                # 写入标注
                f.write(f"{class_names.index(class_name)} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")
