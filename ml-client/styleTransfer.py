import tensorflow_hub as hub
import tensorflow as tf
from io import BytesIO
import numpy as np
import functools
import filetype
import PIL.Image 
import base64
import os

def initialize():
    return hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

def crop_center(image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[1], shape[2])
    offset_y = max(shape[1] - shape[2], 0) // 2
    offset_x = max(shape[2] - shape[1], 0) // 2
    image = tf.image.crop_to_bounding_box(image, offset_y, offset_x, new_shape, new_shape)
    return image

@functools.lru_cache(maxsize=None)
def load_image(image_url, image_size=(256, 256), preserve_aspect_ratio=True):
    """Loads and preprocesses images."""
    # Cache image file locally.
    image_path = tf.keras.utils.get_file(os.path.basename(image_url)[-128:], image_url)
    # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
    img = tf.io.decode_image(tf.io.read_file(image_path), channels=3, dtype=tf.float32)[tf.newaxis, ...]
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img

@functools.lru_cache(maxsize=None)
def load_uploaded_image(imageBytes, image_size=(256, 256), preserve_aspect_ratio=True):
    img = tf.io.decode_image(imageBytes, channels=3, dtype=tf.float32)[tf.newaxis, ...]
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img

def url_perform_style_transfer(model, content_image_url, style_image_url):
    error = []
    try:
        content_image = load_image(content_image_url, (700, 700))
    except:
        error.append("content")
    try:
        style_image = load_image(style_image_url, (256, 256))
    except:
        error.append("style")
    if(len(error) > 0):
        return error
    style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')
    outputs = model(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]
    stylized_image *= 255
    stylized_image = np.array(stylized_image, dtype=np.uint8)
    result = PIL.Image.fromarray(stylized_image[0])
    buffered = BytesIO()
    result.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return "data:image/" + filetype.guess(buffered).extension + ";base64," + img_str.decode()

def uploaded_perform_style_transfer(model, uploaded_content_image, uploaded_style_image):
    content_image = load_uploaded_image(uploaded_content_image, (700, 700))
    style_image = load_uploaded_image(uploaded_style_image, (256, 256))
    style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')
    outputs = model(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]
    stylized_image *= 255
    stylized_image = np.array(stylized_image, dtype=np.uint8)
    result = PIL.Image.fromarray(stylized_image[0])
    buffered = BytesIO()
    result.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    stylized_image_URI = "data:image/" + filetype.guess(buffered).extension + ";base64," + img_str.decode()
    return stylized_image_URI