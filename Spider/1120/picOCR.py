from PIL import Image
import pytesseract


#二值化图像传入图像和阈值
def erzhihua(image, threshold):
    ''':type image:Image.Image'''
    image = image.convert('L')
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return image.point(table, '1')


def pic_orc(path):
    im = Image.open(path)
    image = erzhihua(im, 90)
    # image.show()
    pytesseract.pytesseract.tesseract_cmd = 'c://Program Files (x86)//Tesseract-OCR//tesseract.exe'
    tessdata_dir_config = '--tessdata-dir "c://Program Files (x86)//Tesseract-OCR//tessdata"'
    result = pytesseract.image_to_string(image, lang='eng', config=tessdata_dir_config)
    print(result)


if __name__ == '__main__':
    pic_orc(path='02.png')