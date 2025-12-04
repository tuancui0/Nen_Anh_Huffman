# gui/components.py
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# from core.utils import format_bytes # Không cần vì app.py đã format rồi

class ComparisonRow(ctk.CTkFrame):
    def __init__(self, master, orig_img, rle_img, huff_img, stats):
        super().__init__(master, fg_color="transparent")
        self.pack(fill="x", pady=20, padx=40)

        # Tạo 3 cột
        for i, (title, img, color) in enumerate([
            ("ẢNH GỐC", orig_img, "#dc2626"),
            ("RLE", rle_img, "#3b82f6"),
            ("HUFFMAN", huff_img, "#16a34a")
        ]):
            frame = ctk.CTkFrame(self, corner_radius=16, fg_color="#1f2937" if i > 0 else "#1e293b")
            frame.grid(row=0, column=i, padx=15, sticky="nsew")

            # Tiêu đề
            ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=20, weight="bold"), text_color=color).pack(
                pady=(16, 8))

            # Ảnh
            fig = plt.Figure(figsize=(6, 6), facecolor="#1f2937")
            ax = fig.add_subplot(111)
            ax.imshow(img)
            ax.axis("off")
            canvas = FigureCanvasTkAgg(fig, frame)
            canvas.get_tk_widget().pack(pady=10)

            # Thông tin
            info = stats[i]

            # Khởi tạo chuỗi hiển thị
            text = f"Kích thước file: {info['file']}\n" \
                   f"Dữ liệu thô (chuẩn): {info['raw_standard']}\n"  # Hiển thị kích thước thô chuẩn (phải giống nhau)

            # Chỉ hiển thị Kích thước NÉN cho RLE và Huffman
            if 'compressed' in info:
                text += f"Kích thước NÉN: {info['compressed']}\n"

            text += f"Tỉ lệ nén: {info['ratio']}\n" \
                    f"Thời gian: {info['time']}"

            ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=12), text_color="#e2e8f0", justify="left").pack(
                pady=(0, 16))

        # Cân bằng cột
        self.grid_columnconfigure((0, 1, 2), weight=1)


class ImageCard:
    pass