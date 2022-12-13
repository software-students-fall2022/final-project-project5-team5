from styleTransfer import *
import tensorflow as tf
import pytest

def test_initialize():
    model = initialize()
    assert model != None

def test_crop_center():
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Golden_Gate_Bridge_from_Battery_Spencer.jpg/640px-Golden_Gate_Bridge_from_Battery_Spencer.jpg"
    image_path = tf.keras.utils.get_file(os.path.basename(image_url)[-128:], image_url)
    img = tf.io.decode_image(tf.io.read_file(image_path), channels=3, dtype=tf.float32)[tf.newaxis, ...]
    img = crop_center(img)
    assert type(img) != None
    
def test_load_image():
    img = load_image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Golden_Gate_Bridge_from_Battery_Spencer.jpg/640px-Golden_Gate_Bridge_from_Battery_Spencer.jpg", (256, 256))
    assert type(img) != None

def test_load_uploaded_image():
    imagePath = "./static/images/oceanbeach+-+9.jpeg"
    img = load_uploaded_image(imagePath, (256, 256))
    assert type(img) != None

def test_url_perform_style_transfer():
    model = initialize()
    content_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Golden_Gate_Bridge_from_Battery_Spencer.jpg/640px-Golden_Gate_Bridge_from_Battery_Spencer.jpg"
    style_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/640px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg"
    uri = url_perform_style_transfer(model, content_image_url, style_image_url)
    assert type(uri) is str

def test_uploaded_perform_style_transfer():
    model = initialize()
    uploaded_content_image = "./static/images/pngtree-tennis-ball-png-image_1078825.jpeg"
    uploaded_style_image = "./static/images/oceanbeach+-+9.jpeg"
    images = uploaded_perform_style_transfer(model, uploaded_content_image, uploaded_style_image)
    assert type(images[0]) is str
    assert type(images[1]) is str
    assert type(images[2]) is str
