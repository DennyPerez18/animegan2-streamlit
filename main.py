import base64
from io import BytesIO
import torch
import streamlit as st
from PIL import Image

from utils import create_side_by_side_image


REPO = "bryandlee/animegan2-pytorch:main"
face2paint = torch.hub.load(REPO, "face2paint", size=512)

trained_models_names = [
    "celeba_distill",
    "face_paint_512_v1",
    "face_paint_512_v2",
    "paprika",
]
trained_models = {
    name: torch.hub.load(REPO, "generator", pretrained=name)
    for name in trained_models_names
}

st.title("AnimeGANv2")

selected_model = st.sidebar.selectbox(
    "Trained model to use:", trained_models_names, 2)

img_file = st.file_uploader("Upload an image ( Recommended 512x512 ):")

if img_file is not None:
    original_img = Image.open(img_file).convert("RGB")
    model = trained_models[selected_model]
    trained_img = face2paint(model, original_img)

    buffered = BytesIO()
    trained_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    st.sidebar.download_button(
        "Download trained image as PNG", img_str, mime="image/png")

    plotly_chart = create_side_by_side_image(original_img, trained_img)
    st.plotly_chart(plotly_chart)
