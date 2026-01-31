from typing import Tuple
import cv2
from PIL import Image, ImageTk


def bgr_to_tk_photo(bgr_img, max_size: Tuple[int, int]):
    """
    Convert an OpenCV BGR image to a Tkinter-compatible PhotoImage,
    and resize it proportionally to fit within max_size.
    """
    rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    pil_img.thumbnail(max_size)
    return ImageTk.PhotoImage(pil_img)
