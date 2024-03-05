import argparse
import pypdf
import pytesseract
import textract
from pandas import DataFrame

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
                text += pytesseract.image_to_string(image.image, lang=lang)
                text += '\n'
        else:
            print('Зашли')
            text += page.extract_text()
            # text += '\n' * 2
        
        texts.append(text)
        count += 1
    
    return DataFrame({'page_number': page_number, 'texts': texts})

parser = argparse.ArgumentParser(description='Сканируем текст из документа')

parser.add_argument('type_file', type=str, help='Тип документа: pdf или docx')

parser.add_argument('path_to_file', type=str, help='Путь до файла')

parser.add_argument(
    '--scan',
    type=bool,
    default=False,
    help='Является ли PDF сканом (сканируем текст с изображений) (default: False)'
)

parser.add_argument(
    '--lang',
    type=str,
    default='eng+rus',
    help="язык, используемый в PDF (параметр актуален только при `scan=True`). Возможные значения - `['eng+rus', 'eng', 'rus']`"
)

parser.add_argument(
    '--output_name',
    type=str,
    default='output',
    help="Название выходного файла (БЕЗ `.РАСШИРЕНИЕ_ФАЙЛА`)"
)

args = parser.parse_args()

print(args)


# path_to_file = 'Заметка 15 февр. 2024 г.17_39_43.pdf'

if args.type_file == 'pdf':
    df = read_text_from_pdf(args.path_to_file, scan=args.scan, lang = args.lang)
    df.to_csv(f'{args.output_name}.csv', index=False)
    print(df)
elif args.type_file == 'doc' or args.type_file == 'docx':
    text = textract.process(args.path_to_file).decode("utf-8")
    with open(f"{args.output_name}.txt", "w") as text_file:
        text_file.write(text)
    print(text)