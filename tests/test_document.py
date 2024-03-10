
import argparse
import pypdf
import pytesseract
import textract
from pandas import DataFrame
from PIL import Image
import tempfile
import cv2
import numpy as np
import pandas as pd

def transorm_image_for_ocr(img):

    def remove_noise(img):
        return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)

    def get_grayscale(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # конвертируем изображение в чёрно-белое
    def thresholding(img):
        return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    img_to_transform = np.array(img)

    # нормализуем изображение
    norm_img = np.zeros((img_to_transform.shape[0], img_to_transform.shape[1]))
    img1 = cv2.normalize(img_to_transform, norm_img, 0, 255, cv2.NORM_MINMAX)

    img2 = remove_noise(img1)

    img3 = get_grayscale(img2)

    img4 = thresholding(img3)

    # https://stackoverflow.com/questions/10965417/how-to-convert-a-numpy-array-to-pil-image-applying-matplotlib-colormap
    return Image.fromarray(np.uint8(img4)).convert('RGB')

def read_text_from_pdf(path_to_file:str, scan:bool=False, lang:str='eng+rus'):
    """
    Читаем текст PDF

    * `path_to_file` - путь до файла pdf
    * `scan` - является ли PDF сканом (сканируем текст с изображений)
    * `lang` - язык, используемый в PDF (параметр актуален только при `scan=True`). Возможные значения - `['eng+rus', 'eng', 'rus']`
    """

    pdfFileObj = open(path_to_file, 'rb')

    pdfReader = pypdf.PdfReader(pdfFileObj)

    texts = []
    page_number = []
    count = 1

    for page in pdfReader.pages:
        text = ''
        page_number.append(count)
        if scan:
            for image in page.images:
                text += pytesseract.image_to_string(transorm_image_for_ocr(image.image), lang=lang)
                text += '\n'
        else:
            print('Зашли')
            text += page.extract_text()
            # text += '\n' * 2

        texts.append(text)
        count += 1

    return DataFrame({'page_number': page_number, 'texts': texts})

def test_rus_text():
  out_1 = read_text_from_pdf('./content/рус_текст.pdf',False, 'rus')
  true_df = pd.read_csv('test1.csv')
  assert out_1.equals(true_df)

def test_en_text():
  out_2 = read_text_from_pdf('./content/английский с картинками.pdf',False, 'eng') # dataframe
  true_df = pd.read_csv('test2.csv')
  assert out_2.equals(true_df)

def test_img_eng():
  out_3 = read_text_from_pdf('./content/картинка_английский.pdf',True, 'eng') # dataframe
  true_df = pd.read_csv('test3.csv')
  assert out_3.equals(true_df)

def test_img_ru():
  out_4 = read_text_from_pdf('./content/картинка_русский.pdf',True, 'rus') # dataframe
  true_df = pd.read_csv('test4.csv')
  assert out_4.equals(true_df)

def test_none():
  out_5 = read_text_from_pdf('./content/пусто.pdf',False, 'rus') # dataframe
  true_df = pd.read_csv('test5.csv')
  assert out_5.equals(true_df)

def test_img_china():
  out_6 = read_text_from_pdf('./content/картинка_китайский.pdf',True, 'eng+rus') # dataframe
  true_df = pd.read_csv('test5.csv')
  assert out_6.equals(true_df)
