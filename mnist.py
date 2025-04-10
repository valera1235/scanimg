import numpy as np
import cv2
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical

# 1. Загрузка и подготовка данных MNIST
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# Нормализация и добавление размерности канала
X_train = X_train.reshape((60000, 28, 28, 1)).astype('float32') / 255
X_test = X_test.reshape((10000, 28, 28, 1)).astype('float32') / 255

# Преобразование меток в one-hot encoding
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# 2. Создание модели CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(100, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# 3. Обучение модели
model.fit(X_train, y_train, epochs=5, batch_size=64, validation_data=(X_test, y_test))


# 4. Функция для распознавания цифры с изображения
def recognize_digit(image_path):
    # Загрузка и предварительная обработка изображения
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return "Не удалось загрузить изображение"

    # Инвертирование и нормализация
    img = cv2.bitwise_not(img)
    img = cv2.resize(img, (28, 28))
    img = img.reshape(1, 28, 28, 1).astype('float32') / 255

    # Предсказание
    pred = model.predict(img)
    digit = np.argmax(pred)
    confidence = np.max(pred)

    return digit, confidence


# 5. Пример использования
image_path = 'digit_5.png'  # Замените на путь к вашему изображению
digit, confidence = recognize_digit(image_path)
print(f"Распознанная цифра: {digit} (Уверенность: {confidence:.2%})")