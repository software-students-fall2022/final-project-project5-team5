import numpy as np
from PIL import Image
import tensorflow as tf
import tensorflow_hub

def initialize():
    return tensorflow_hub.load("https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2")

def perform_style_transfer(model, content_image, style_image):
    print(type(content_image))
    content_image = tf.convert_to_tensor(content_image, np.float32)[tf.newaxis, ...] / 255.0
    style_image = tf.convert_to_tensor(style_image, np.float32)[tf.newaxis, ...] / 255.0

    stylized_image = model(content_image, style_image)[0]
    
    return Image.fromarray(np.uint8(stylized_image[0] * 255))

