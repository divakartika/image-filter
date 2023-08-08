import cv2
import streamlit as st
import numpy as np

st.set_page_config(
    page_title="OpenCV Image Filters",
    page_icon="https://raw.githubusercontent.com/wiki/opencv/opencv/logo/OpenCV_logo_no_text.png",
    initial_sidebar_state="expanded"
)

def brighten_image(image, amount):
    img_bright = cv2.convertScaleAbs(image, beta=amount)
    return img_bright


def blur_image(image, amount):
    blur_img = cv2.GaussianBlur(image, (11, 11), amount)
    return blur_img


def enhance_details(img):
    hdr = cv2.detailEnhance(img, sigma_s=12, sigma_r=0.15)
    return hdr


def main_loop():
    st.title("OpenCV Image Filters")
    st.subheader("This app allows you to play with Image filters!")

    input_type = st.sidebar.radio(
        "How do you want to input your image?",
        ('Upload image', 'Webcam capture'))

    if input_type == 'Webcam capture':
        capture = True
        upload = False
    else:
        capture = False
        upload = True

    blur_rate = st.sidebar.slider("Blurring", min_value=0.5, max_value=3.5)
    brightness_amount = st.sidebar.slider("Brightness", min_value=-50, max_value=50, value=0)
    apply_enhancement_filter = st.sidebar.checkbox('Enhance Details')

    if capture:
        image_file = st.camera_input("Take a picture")
        if not image_file:
            return None
    elif upload:
        image_file = st.file_uploader("Upload Your Image", type=['jpg', 'png', 'jpeg'])
        if not image_file:
            return None
    else:
        return None

    col1, col2 = st.columns(2)

    if image_file:
        col1.text("Original Image")
        col1.image(image_file)
    else:
        return None
    
    bytes_data = image_file.getvalue()
    original_image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    processed_image = blur_image(rgb, blur_rate)
    processed_image = brighten_image(processed_image, brightness_amount)

    if apply_enhancement_filter:
        processed_image = enhance_details(processed_image)

    col2.text("Processed Image")
    col2.image(processed_image)


if __name__ == '__main__':
    main_loop()