import torch
import streamlit as st
from PIL import Image

from utils import create_side_by_side_image, save_pil_image_as_bytes


TRAINED_MODELS_NAMES = [
    "celeba_distill",
    "face_paint_512_v1",
    "face_paint_512_v2",
    "paprika",
]

# This is not really necessary, since
# torchhub already caches the models, but
# the app logs at least will be cleaner.
@st.cache(suppress_st_warning=True)
def torchhub_repos_cache(models_names):
    REPO = "bryandlee/animegan2-pytorch:main"
    face2paint = torch.hub.load(REPO, "face2paint", size=512)
    trained_models = {
        name: torch.hub.load(REPO, "generator", pretrained=name)
        for name in models_names
    }
    return face2paint, trained_models


face2paint, trained_models = torchhub_repos_cache(TRAINED_MODELS_NAMES)

st.title("AnimeGANv2")

selected_model = st.sidebar.selectbox(
    "Trained model to use:",
    TRAINED_MODELS_NAMES, 2
)

img_file = st.file_uploader("Upload an image ( Recommended 512x512 ):")

# todo: Add loading bar...
if img_file is not None:
    original_img = Image.open(img_file).convert("RGB")

    model = trained_models[selected_model]
    trained_img = face2paint(model, original_img)

    plotly_chart = create_side_by_side_image(original_img, trained_img)
    st.plotly_chart(plotly_chart)

    st.sidebar.download_button(
        "Download trained image as PNG",
        save_pil_image_as_bytes(trained_img),
        mime="image/png"
    )
