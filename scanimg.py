from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# Загрузка предобученной модели
model = VGG16(weights='imagenet')

# Загрузка и предобработка изображения
image = load_img('path_to_image.jpg', target_size=(224, 224))
image = img_to_array(image)
image = np.expand_dims(image, axis=0)
image = preprocess_input(image)

# Классификация изображения
predictions = model.predict(image)
label = decode_predictions(predictions)
print(label)