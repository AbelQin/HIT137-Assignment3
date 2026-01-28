import cv2
import numpy as np


class ImageProcessor:
    """OpenCV 图像处理功能集合（Methods）"""

    @staticmethod
    def to_grayscale(bgr: np.ndarray) -> np.ndarray:
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def gaussian_blur(bgr: np.ndarray, intensity: int) -> np.ndarray:
        # intensity: 0~20 -> kernel: 1,3,5...
        k = max(1, int(intensity) * 2 + 1)
        return cv2.GaussianBlur(bgr, (k, k), 0)

    @staticmethod
    def canny_edges(bgr: np.ndarray, t1: int = 80, t2: int = 160) -> np.ndarray:
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, t1, t2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def adjust_brightness(bgr: np.ndarray, beta: int) -> np.ndarray:
        # beta: -100 ~ +100
        return cv2.convertScaleAbs(bgr, alpha=1.0, beta=beta)

    @staticmethod
    def adjust_contrast(bgr: np.ndarray, alpha: float) -> np.ndarray:
        # alpha: 0.2 ~ 3.0
        return cv2.convertScaleAbs(bgr, alpha=alpha, beta=0)

    @staticmethod
    def rotate(bgr: np.ndarray, angle: int) -> np.ndarray:
        if angle == 90:
            return cv2.rotate(bgr, cv2.ROTATE_90_CLOCKWISE)
        if angle == 180:
            return cv2.rotate(bgr, cv2.ROTATE_180)
        if angle == 270:
            return cv2.rotate(bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)
        raise ValueError("只支持 90/180/270 度旋转。")

    @staticmethod
    def flip(bgr: np.ndarray, mode: str) -> np.ndarray:
        if mode == "horizontal":
            return cv2.flip(bgr, 1)
        if mode == "vertical":
            return cv2.flip(bgr, 0)
        raise ValueError("flip 模式应为 horizontal 或 vertical。")

    @staticmethod
    def resize_scale(bgr: np.ndarray, scale: float) -> np.ndarray:
        # scale: 0.1 ~ 2.0
        h, w = bgr.shape[:2]
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        interp = cv2.INTER_AREA if scale < 1 else cv2.INTER_CUBIC
        return cv2.resize(bgr, (new_w, new_h), interpolation=interp)
