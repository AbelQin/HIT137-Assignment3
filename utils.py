from typing import Tuple
import cv2
from PIL import Image, ImageTk


def bgr_to_tk_photo(bgr_img, max_size: Tuple[int, int]):
    """
    将 OpenCV BGR 转为 Tkinter 可显示的 PhotoImage，并按 max_size 等比缩放。
    """
    rgb = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    pil_img.thumbnail(max_size)
    return ImageTk.PhotoImage(pil_img)
