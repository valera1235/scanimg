import cv2
import numpy as np
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image


def recognize_number_with_vgg16(image_path):
    # Загружаем предобученную модель VGG16
    model = VGG16(weights='imagenet')

    # Загружаем и подготавливаем изображение
    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    # Делаем предсказание
    preds = model.predict(x)

    # Декодируем и выводим топ-3 предсказания
    decoded_preds = decode_predictions(preds, top=3)[0]

    print("Предсказания VGG16:")
    for i, (imagenet_id, label, score) in enumerate(decoded_preds):
        print(f"{i + 1}: {label} ({score:.2f})")

    return decoded_preds
