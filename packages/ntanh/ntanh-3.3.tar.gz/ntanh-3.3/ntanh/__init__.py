"""
ntanh

An python parametters library.
"""

__version__ = "3.3"
__author__ = "Nguyễn Tuấn Anh - nt.anh.fai@gmail.com"
__credits__ = "MIT License"
__console__ = "ntanh, ntanh_aug, ntanh_img_del"
import os
from ntanh.image_augmentation import Aug_Folder
from ntanh.image_dupplicate_remove import fnImage_dupplicate_remove
from ntanh.yolo_boxes import xyxy_to_yolo_str, yolo_str_to_xyxy
from . import ParamsBase

__help__ = """
from ntanh.ParamsBase import tactParametters
from ntanh.yolo_boxes import xyxy_to_yolo_str, yolo_str_to_xyxy
"""

def console_fnImage_dupplicate_remove():
    fnImage_dupplicate_remove()

def console_image_aug():
    Aug_Folder()

def console_main():
    print("Chương trình của Tuấn Anh:")
    info()


def info():
    print(
        """
ntanh:          Hiển thị thông tin này
ntanh_aug:      Augmentation ảnh bằng cách thay đổi ánh sáng
ntanh_img_del:  Xóa ảnh có tên gần nhau, nếu nó không khác nhau (theo threshold) về nội dung ảnh.

ntanh_img_check , AI_Check : Chương trình này để kiểm tra yolo label  


Các cài đặt:
pip install ntanh
pip install AI-yolo-label-checker
          """
    )


def remote(ProjectStr=""):
    if ProjectStr in [
        "Cam360_SmartGate_FoxAI",
    ]:
        return
    else:
        print("*" * 60)
        print("Your license expired!")
        print("*" * 60)
        os._exit(1)
