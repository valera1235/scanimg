import easyocr
import cv2
import numpy as np

def recognize_numbers_with_easyocr(image_path, language='en'):
    # Инициализация EasyOCR (английский язык по умолчанию)
    reader = easyocr.Reader([language])  

    # Чтение изображения
    image = cv2.imread(image_path)
    if image is None:
        return "Ошибка: не удалось загрузить изображение"

    # Распознавание текста (цифр)
    results = reader.readtext(image, allowlist='0123456789')  # Разрешаем только цифры

    # Обработка результатов
    recognized_numbers = []
    for (bbox, text, confidence) in results:
        recognized_numbers.append({
            'text': text,
            'confidence': float(confidence),
            'position': np.array(bbox).tolist()  # Координаты bounding box
        })

        # Визуализация (опционально)
        cv2.rectangle(image, 
                      tuple(map(int, bbox[0])),  # Верхний левый угол
                      tuple(map(int, bbox[2])),  # Нижний правый угол
                      (0, 255, 0), 2)  # Зеленый прямоугольник

    # Показать изображение с выделенными цифрами (опционально)
    cv2.imshow('Recognized Numbers', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return recognized_numbers

# Пример использования
image_path = 'numbers.jpg'  # Замените на свой файл
numbers = recognize_numbers_with_easyocr(image_path)

print("Распознанные числа:")
for num in numbers:
    print(f"Цифра: {num['text']} | Уверенность: {num['confidence']:.2%} | Позиция: {num['position']}")
