from typing import Optional
import cv2
import numpy as np


class ImageModel:
    def __init__(self):
        self.original_bgr: Optional[np.ndarray] = None
        self.committed_bgr: Optional[np.ndarray] = None
        self.current_bgr: Optional[np.ndarray] = None
        self.path: Optional[str] = None

    def has_image(self) -> bool:
        return self.current_bgr is not None

    def load(self, path: str) -> None:
        img = cv2.imread(path)
        if img is None:
            raise ValueError("Unable to read the image. Please choose a common format (jpg/png/bmp, etc.).")
        self.path = path
        self.original_bgr = img
        self.committed_bgr = img.copy()
        self.current_bgr = img.copy()

    def reset(self) -> None:
        if self.original_bgr is not None:
            self.committed_bgr = self.original_bgr.copy()
            self.current_bgr = self.original_bgr.copy()

    def get_current(self) -> Optional[np.ndarray]:
        return self.current_bgr

    def get_committed(self) -> Optional[np.ndarray]:
        """Return the base image used for slider-based adjustments."""
        return self.committed_bgr

    def set_current(self, bgr_img: np.ndarray) -> None:
        self.current_bgr = bgr_img

    def commit(self, bgr_img: np.ndarray) -> None:
        """Commit the result of a button operation as the new base image."""
        self.committed_bgr = bgr_img
        self.current_bgr = bgr_img

    def save(self, out_path: str) -> None:
        if not self.has_image():
            raise ValueError("There is no image to save.")
        ok = cv2.imwrite(out_path, self.current_bgr)
        if not ok:
            raise ValueError("Failed to save the image. Please check the path or permissions.")
