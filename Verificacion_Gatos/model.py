import numpy as np
import tf_keras as keras
from PIL import Image


def get_class(model_path, labels_path, image_path):

    # Cargar el modelo de Teachable Machine
    model = keras.models.load_model(
        model_path,
        compile=False
    )

    # Cargar las etiquetas
    with open(labels_path, "r", encoding="utf-8") as file:
        class_names = [line.strip() for line in file.readlines()]

    # Abrir la imagen
    image = Image.open(image_path).convert("RGB")

    # Teachable Machine utiliza imágenes de 224x224
    image = image.resize((224, 224))

    # Convertir imagen a números
    image_array = np.asarray(image)

    # Normalizar los valores
    normalized_image = (
        image_array.astype(np.float32) / 127.5
    ) - 1

    # Crear entrada para el modelo
    data = np.ndarray(
        shape=(1, 224, 224, 3),
        dtype=np.float32
    )

    data[0] = normalized_image

    # Realizar predicción
    prediction = model.predict(data, verbose=0)

    # Obtener la clase con mayor probabilidad
    index = np.argmax(prediction[0])

    class_name = class_names[index]
    confidence = prediction[0][index]

    return f"{class_name} ({confidence * 100:.2f}%)"