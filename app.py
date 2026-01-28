import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from model import ImageModel
from processor import ImageProcessor
from utils import bgr_to_tk_photo


class ImageEditorApp:
    """
    GUI + 类交互（Class Interaction）
    - 控制 ImageModel 与 ImageProcessor
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("OOP Image Editor (Tkinter + OpenCV)")
        self.root.geometry("1100x650")

        self.model = ImageModel()
        self.preview_photo = None  # 防止被回收

        self._build_ui()
        self.root.bind("<Configure>", self._on_resize)

    def _build_ui(self):
        top = ttk.Frame(self.root, padding=8)
        top.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(top, text="打开图片", command=self.open_image).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="保存输出", command=self.save_image).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="重置为原图", command=self.reset_image).pack(side=tk.LEFT, padx=4)

        ttk.Separator(top, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        ttk.Button(top, text="灰度", command=self.apply_grayscale).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="边缘检测(Canny)", command=self.apply_edges).pack(side=tk.LEFT, padx=4)

        mid = ttk.Frame(self.root, padding=8)
        mid.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.controls = ttk.LabelFrame(mid, text="参数控制", padding=10)
        self.controls.pack(side=tk.LEFT, fill=tk.Y)

        self.preview = ttk.LabelFrame(mid, text="预览", padding=10)
        self.preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.preview_label = ttk.Label(self.preview)
        self.preview_label.pack(fill=tk.BOTH, expand=True)

        # 模糊
        ttk.Label(self.controls, text="模糊强度 (Gaussian)").pack(anchor="w")
        self.blur_var = tk.IntVar(value=0)
        ttk.Scale(self.controls, from_=0, to=20, variable=self.blur_var,
                  command=lambda e: self.apply_blur()).pack(fill=tk.X, pady=(0, 10))

        # 亮度
        ttk.Label(self.controls, text="亮度 (-100 ~ +100)").pack(anchor="w")
        self.brightness_var = tk.IntVar(value=0)
        ttk.Scale(self.controls, from_=-100, to=100, variable=self.brightness_var,
                  command=lambda e: self.apply_brightness_contrast()).pack(fill=tk.X, pady=(0, 10))

        # 对比度
        ttk.Label(self.controls, text="对比度 (0.2 ~ 3.0)").pack(anchor="w")
        self.contrast_var = tk.DoubleVar(value=1.0)
        ttk.Scale(self.controls, from_=0.2, to=3.0, variable=self.contrast_var,
                  command=lambda e: self.apply_brightness_contrast()).pack(fill=tk.X, pady=(0, 10))

        ttk.Separator(self.controls).pack(fill=tk.X, pady=8)

        # 旋转
        ttk.Label(self.controls, text="旋转").pack(anchor="w")
        rot_row = ttk.Frame(self.controls)
        rot_row.pack(fill=tk.X, pady=(4, 10))
        ttk.Button(rot_row, text="90°", command=lambda: self.apply_rotate(90)).pack(side=tk.LEFT, padx=2)
        ttk.Button(rot_row, text="180°", command=lambda: self.apply_rotate(180)).pack(side=tk.LEFT, padx=2)
        ttk.Button(rot_row, text="270°", command=lambda: self.apply_rotate(270)).pack(side=tk.LEFT, padx=2)

        # 翻转
        ttk.Label(self.controls, text="翻转").pack(anchor="w")
        flip_row = ttk.Frame(self.controls)
        flip_row.pack(fill=tk.X, pady=(4, 10))
        ttk.Button(flip_row, text="水平翻转", command=lambda: self.apply_flip("horizontal")).pack(side=tk.LEFT, padx=2)
        ttk.Button(flip_row, text="垂直翻转", command=lambda: self.apply_flip("vertical")).pack(side=tk.LEFT, padx=2)

        ttk.Separator(self.controls).pack(fill=tk.X, pady=8)

        # 缩放
        ttk.Label(self.controls, text="缩放比例 (0.1 ~ 2.0)").pack(anchor="w")
        self.scale_var = tk.DoubleVar(value=1.0)
        ttk.Scale(self.controls, from_=0.1, to=2.0, variable=self.scale_var).pack(fill=tk.X, pady=(0, 4))
        ttk.Button(self.controls, text="应用缩放", command=self.apply_scale).pack(fill=tk.X, pady=(0, 10))

        self.status = tk.StringVar(value="提示：先点击“打开图片”。保存建议输出到 outputs/ 文件夹。")
        ttk.Label(self.root, textvariable=self.status, padding=8).pack(side=tk.BOTTOM, fill=tk.X)

    # ---------- 基础 ----------
    def _require_image(self) -> bool:
        if not self.model.has_image():
            messagebox.showwarning("提示", "请先打开一张图片。")
            return False
        return True

    def _render_preview(self):
        bgr = self.model.get_current()
        if bgr is None:
            return

        frame_w = max(200, self.preview.winfo_width() - 40)
        frame_h = max(200, self.preview.winfo_height() - 60)

        self.preview_photo = bgr_to_tk_photo(bgr, (frame_w, frame_h))
        self.preview_label.configure(image=self.preview_photo)

    def _reset_sliders(self):
        self.blur_var.set(0)
        self.brightness_var.set(0)
        self.contrast_var.set(1.0)
        self.scale_var.set(1.0)

    def _on_resize(self, event):
        if self.model.has_image():
            self._render_preview()

    # ---------- 文件操作 ----------
    def open_image(self):
        path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff"), ("All Files", "*.*")]
        )
        if not path:
            return
        try:
            self.model.load(path)
            self._reset_sliders()
            self._render_preview()
            self.status.set(f"已加载：{os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def save_image(self):
        if not self._require_image():
            return

        os.makedirs("outputs", exist_ok=True)
        path = filedialog.asksaveasfilename(
            title="保存输出",
            defaultextension=".png",
            initialdir="outputs",
            initialfile="edited_output.png",
            filetypes=[("PNG", "*.png"), ("JPG", "*.jpg;*.jpeg"), ("BMP", "*.bmp"), ("All Files", "*.*")]
        )
        if not path:
            return
        try:
            self.model.save(path)
            self.status.set(f"已保存输出：{path}")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def reset_image(self):
        if not self.model.has_image():
            return
        self.model.reset()
        self._reset_sliders()
        self._render_preview()
        self.status.set("已重置为原图。")

    # ---------- 功能 ----------
    def apply_grayscale(self):
        if not self._require_image():
         return
        out = ImageProcessor.to_grayscale(self.model.get_current())
        self.model.commit(out)          # ✅ 提交为新基底
        self._reset_sliders()           # ✅ 清空滑条
        self._render_preview()
        self.status.set("已应用：灰度转换。")

    def apply_blur(self):
         if not self._require_image():
          return
         self._apply_adjustments()
         self.status.set(f"预览：模糊强度={int(self.blur_var.get())}")

    def apply_edges(self):
      if not self._require_image():
         return

      base = self.model.get_committed()  # ✅ 用基底图
      out = ImageProcessor.canny_edges(base)  # ✅ Canny 边缘检测

      self.model.commit(out)       # 提交为新基底
      self._reset_sliders()
      self._render_preview()
      self.status.set("已应用：Canny 边缘检测。")


    def apply_brightness_contrast(self):
      if not self._require_image():
        return
      self._apply_adjustments()
      self.status.set(f"预览：亮度={int(self.brightness_var.get())}, 对比度={float(self.contrast_var.get()):.2f}")

    def apply_rotate(self, angle: int):
      if not self._require_image():
        return

      base = self.model.get_committed()   # ✅ 用“基底图”，不是 current
      out = ImageProcessor.rotate(base, angle)

      self.model.commit(out)              # 提交为新基底
      self._reset_sliders()               # 清空滑条
      self._render_preview()

      self.status.set(f"已应用：旋转 {angle}°")

    def apply_flip(self, mode: str):
      if not self._require_image():
        return

      base = self.model.get_committed()  # ✅ 用基底图（彩色、已提交）
      try:
         out = ImageProcessor.flip(base, mode)
      except Exception as e:
         messagebox.showerror("错误", str(e))
         return

      self.model.commit(out)   # ✅ 翻转结果提交为新基底
      self._reset_sliders()    # ✅ 清空滑条预览状态
      self._render_preview()
      self.status.set(f"已应用：翻转 {mode}")


    def apply_scale(self):
        if not self._require_image():
         return
        self._apply_adjustments()
        self.status.set(f"预览：缩放比例={float(self.scale_var.get()):.2f}")

    def _apply_adjustments(self):
      base = self.model.get_committed()
      if base is None:
        return

      img = base.copy()

    # 1) 模糊
      intensity = int(self.blur_var.get())
      if intensity > 0:
          img = ImageProcessor.gaussian_blur(img, intensity)

    # 2) 对比度 + 亮度
      alpha = float(self.contrast_var.get())
      beta = int(self.brightness_var.get())
      if abs(alpha - 1.0) > 1e-6:
         img = ImageProcessor.adjust_contrast(img, alpha)
      if beta != 0:
         img = ImageProcessor.adjust_brightness(img, beta)

    # 3) 缩放（这里做预览缩放；也可以只点“应用缩放”才生效）
    # 如果你希望缩放必须点按钮才生效，就把这段注释掉
      scale = float(self.scale_var.get())
      if abs(scale - 1.0) > 1e-6:
          img = ImageProcessor.resize_scale(img, scale)

      self.model.set_current(img)
      self._render_preview()

