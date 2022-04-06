from io import BytesIO
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def create_side_by_side_image(image1, image2):
    fig = make_subplots(rows=1, cols=2)

    fig.add_trace(go.Image(z=image1), row=1, col=1)
    fig.add_trace(go.Image(z=image2), row=1, col=2)

    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(visible=False, showticklabels=False)

    return fig


def save_pil_image_as_bytes(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return buffered.getvalue()
