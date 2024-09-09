from PIL import Image
import io
import numpy as np
import tensorflow as tf
import time

## Custom Loss Function
def focal_loss(gamma=2., alpha=0.25):
    def focal_loss_fixed(y_true, y_pred):
        epsilon = tf.keras.backend.epsilon()
        y_pred = tf.clip_by_value(y_pred, epsilon, 1. - epsilon)
        y_true = tf.cast(y_true, tf.float32)
        alpha_t = y_true * alpha + (tf.keras.backend.ones_like(y_true) - y_true) * (1 - alpha)
        p_t = y_true * y_pred + (tf.keras.backend.ones_like(y_true) - y_true) * (1 - y_pred)
        fl = - alpha_t * tf.keras.backend.pow((tf.keras.backend.ones_like(y_true) - p_t), gamma) * tf.keras.backend.log(p_t)
        return tf.keras.backend.mean(fl)
    return focal_loss_fixed

model = tf.keras.models.load_model(
    'Model//V1//DiseaseDetectionModel.h5',
    custom_objects={'focal_loss': focal_loss},
    compile=False
)
model.compile(
    optimizer='adam',  
    loss=focal_loss(),  
    metrics=['accuracy']  
)
def process_image(image: Image.Image):
    image = image.resize((256, 256))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Crop Disease Detection model excluding RICE
def predictive_model(image_bytes: bytes):
    request_time = int(time.time())
    
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    input_tensor = process_image(image)
    
    prediction = model.predict(input_tensor)
    
    # Top 4 predictions
    top_indices = np.argsort(prediction[0])[-4:][::-1]
    top_confidences = prediction[0][top_indices]
    top_classes = top_indices
    
    prediction_time = int(time.time())
    
    response = {
        "top_predictions": [
            {"class": int(cls), "confidence_score": float(conf)}
            for cls, conf in zip(top_classes, top_confidences)
        ],
        "request_time": request_time,
        "prediction_time": prediction_time
    }
    
    return response
