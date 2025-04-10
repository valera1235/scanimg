import cv2
import pytesseract
from PIL import Image


# Укажите путь к исполняемому файлу Tesseract OCR, если он не добавлен в PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def recognize_number_from_image(image_path):
    # Загружаем изображение
    img = cv2.imread(image_path)

    # Конвертируем в оттенки серого
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Применяем пороговую обработку (бинаризацию)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Убираем шумы
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    # Распознаем текст (число) с помощью Tesseract OCR
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    number = pytesseract.image_to_string(opening, config=custom_config)

    # Удаляем лишние символы
    number = ''.join(filter(str.isdigit, number))

    return number if number else "Не удалось распознать число"


# Пример использования
image_path = 'number.png'  # Замените на путь к вашему изображению
recognized_number = recognize_number_from_image(image_path)
print(f"Распознанное число: {recognized_number}")