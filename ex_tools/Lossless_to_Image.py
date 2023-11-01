# 图片无损压缩
from PIL import Image
import pyperclip as cb


def compress_image(input_img, output_img, quality=50):
    image = Image.open(input_img)
    image.save(output_img, optimize=True, quality=quality)


if __name__ == '__main__':
    input_image_path = r'G:\照片记录\20200125-全家福\全家福.jpg'
    output_image_path = r'1.jpg'
    compress_image(input_image_path, output_image_path)
