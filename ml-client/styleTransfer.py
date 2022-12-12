from matplotlib import gridspec
import matplotlib.pylab as plt
import tensorflow_hub as hub
import tensorflow as tf
from io import BytesIO
import numpy as np
import functools
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
def load_uploaded_image(image_path, image_size=(256, 256), preserve_aspect_ratio=True):
    img = tf.io.decode_image(tf.io.read_file(image_path), channels=3, dtype=tf.float32)[tf.newaxis, ...]
    img = crop_center(img)
    img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
    return img

#with open("./static/images/178c20b0-f4aa-458a-9524-456a886a736b_1.2e976aeb60135ed768d6be8503d1589d.jpeg", "rb") as tennis:
 #   tennisball = base64.b64encode(tennis.read())
#print("data:image/jpeg;base64," + tennisball.decode())

#tennisball = tf.io.decode_image(tf.io.read_file("./static/images/178c20b0-f4aa-458a-9524-456a886a736b_1.2e976aeb60135ed768d6be8503d1589d.jpeg"), channels=3, dtype=tf.float32)[tf.newaxis, ...]
#print('worked!')

#content_image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Golden_Gate_Bridge_from_Battery_Spencer.jpg/640px-Golden_Gate_Bridge_from_Battery_Spencer.jpg'  # @param {type:"string"}
#style_image_url = 'https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Great_Wave_off_Kanagawa.jpg'  # @param {type:"string"}
#output_image_size = 384  # @param {type:"integer"}

# The content image size can be arbitrary.
#content_img_size = (output_image_size, output_image_size)
# The style prediction model was trained with image size 256 and it's the 
# recommended image size for the style image (though, other sizes work as 
# well but will lead to different results).

def url_perform_style_transfer(model, content_image_url, style_image_url):
    content_image = load_image(content_image_url, (500, 500))
    style_image = load_image(style_image_url, (256, 256))
    style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')
    outputs = model(tf.constant(content_image), tf.constant(style_image))
    stylized_image = outputs[0]
    stylized_image *= 255
    stylized_image = np.array(stylized_image, dtype=np.uint8)
    result = PIL.Image.fromarray(stylized_image[0])
    buffered = BytesIO()
    result.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return "data:image/jpeg;base64," + img_str.decode()

def uploaded_perform_style_transfer(model, uploaded_content_image, uploaded_style_image):
    with open(uploaded_content_image, "rb") as content_image:
        content_image_URI = "data:image/" + uploaded_content_image[uploaded_content_image.rfind(".")+1:] + ";base64," + base64.b64encode(content_image.read()).decode()
    content_image.close()
    with open(uploaded_style_image, "rb") as style_image:
        style_image_URI = "data:image/" + uploaded_style_image[uploaded_style_image.rfind(".")+1:] + ";base64," + base64.b64encode(style_image.read()).decode()
    style_image.close()
    content_image = load_uploaded_image(uploaded_content_image, (500, 500))
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
    stylized_image_URI = "data:image/jpeg;base64," + img_str.decode()
    return (content_image_URI, style_image_URI, stylized_image_URI)