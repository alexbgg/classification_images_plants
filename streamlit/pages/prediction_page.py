import time

import utils
from PIL import Image

import streamlit as st


# Configuration for Luigi's champ
luigi = {
    "model_name": "TL_180px_32b_20e_model.keras",
    "color_mode": "RGB",
    "target_size": (180, 180),
    "interpolation": "BILINEAR",
    "keep_aspect_ratio": False,
}

# Configuration for Bernd's silver champ
bernd = {
    "model_name": "Lenet_64px_32b-200e-model.keras",
    "color_mode": "RGB",
    "target_size": (64, 64),
    "interpolation": "BILINEAR",
    "keep_aspect_ratio": False,
}

# Configuration for my augmented model (AuLex...)
alex = {
    "model_name": "AuLexNet5_128px_gray_32b_100e_model.keras",
    "color_mode": "grayscale",
    "target_size": (128, 128),
    "interpolation": "BILINEAR",
    "keep_aspect_ratio": False,
}

# Mapping model types to their configurations
model_list = {
    "Transfer Learning": luigi,
    "LeNet": bernd,
    "Augmented LeNet": alex,
}


def prediction_home():
    """
    Function to perform image prediction and display results.

    Returns:
        None
    """
    # Initialize session state for previous value if not already initialized
    if "previous_mod_sel_value" not in st.session_state:
        st.session_state.previous_mod_sel_value = None

    if "previous_up_img_value" not in st.session_state:
        st.session_state.previous_up_img_value = None

    if "model_value" not in st.session_state:
        st.session_state.model_value = None

    st.header("Prediction 🍃")
    st.subheader("1. Choose which model you want to use for prediction")

    csb1, _, _ = st.columns(3)
    with csb1:
        selected_model = st.selectbox(
            "Select a model to load:",
            ["Please select a model..."] + list(model_list.keys()),
            key="model_select_box",
        )

        # Conditional content based on the selection
        if selected_model != "Please select a model...":
            if selected_model != st.session_state.previous_mod_sel_value:
                # Update the previous value in the session state
                st.session_state.previous_mod_sel_value = selected_model
                st.session_state.previous_up_img_value = False

                model_file = model_list[selected_model]["model_name"]

                st.write(f"Loading model: {model_file}")
                model = utils.load_model_with_progress("../models/" + model_file)
                st.session_state.model_value = model

                st.success(f"Model {selected_model} loaded successfully!")
                st.write("Now you can use the model for predictions or further analysis:")

            st.write("")
            st.subheader("Upload an image")
            st.markdown("*Note: please don't expect too much and don't load strange image.*")

            image, image_valid = utils.upload_image()
            st.session_state.previous_up_img_value = image_valid

            img_info = Image.open(image)
            file_details = f"""
                Name: {image.name}
                Type: {img_info.format}
                Size: {img_info.size}
            """

            st.write("")
            st.subheader("Results")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original image ...")

                st.image(img_info, width=150)
                if st.session_state.previous_up_img_value:
                    st.caption(file_details)

            with col2:
                with st.container():
                    st.subheader("... is probably :")

                    # Add here the prediction model result.
                    if st.session_state.previous_up_img_value:
                        image_array = utils.preprocess_image(img_info, model_list[selected_model])
                        pred_classes = utils.predict(st.session_state.model_value, image_array)
                        print(pred_classes)
        else:
            print("Conditional content based on the selection")
