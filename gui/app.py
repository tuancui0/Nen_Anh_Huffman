# gui/app.py
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import os, time, uuid
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core.rle import RLECompressor
from core.huffman import HuffmanCompressor
from core.utils import calculate_mse_psnr, format_bytes
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ImageCompressionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nén Ảnh Lossless - RLE vs Huffman")
        self.geometry("1700x1000")

        self.compressors = {"RLE": RLECompressor(), "Huffman": HuffmanCompressor()}
        self.img = None
        self.shape = None
        self.results = {}

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self, height=100, fg_color="#0f172a", corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="NÉN ẢNH KHÔNG MẤT DỮ LIỆU", font=ctk.CTkFont(size=28, weight="bold"), text_color="#e2e8f0").pack(pady=20)
        ctk.CTkLabel(header, text="So sánh RLE & Huffman - Lossless 100%", text_color="#94a3b8").pack()

        # Controls
        controls = ctk.CTkFrame(self)
        controls.pack(pady=20, padx=40, fill="x")

        ctk.CTkButton(controls, text="CHỌN ẢNH", height=45, font=ctk.CTkFont(weight="bold"), command=self.load_image).pack(side="left", padx=10)
        self.btn_verify = ctk.CTkButton(controls, text="KIỂM TRA LOSSLESS", state="disabled", command=self.verify)
        self.btn_verify.pack(side="left", padx=10)
        self.btn_export = ctk.CTkButton(controls, text="XUẤT FILE", state="disabled", command=self.show_export_menu)
        self.btn_export.pack(side="left", padx=10)

        self.progress = ctk.CTkProgressBar(controls)
        self.progress.pack(fill="x", padx=40, pady=15)
        self.progress.set(0)

        # Results
        self.result_area = ctk.CTkScrollableFrame(self, fg_color="#f8fafc")
        self.result_area.pack(fill="both", expand=True, padx=40, pady=10)

        # Footer
        footer = ctk.CTkFrame(self, height=40, fg_color="#1e293b", corner_radius=0)
        footer.pack(fill="x")
        footer.pack_propagate(False)
        ctk.CTkLabel(footer, text="© 2025 - Đồ án Nén Ảnh Lossless", text_color="#94a3b8").pack(pady=10)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image", "*.png *.jpg *.jpeg *.bmp")])
        if not path: return
        try:
            img = Image.open(path).convert("RGB")
            self.img = np.array(img, dtype=np.uint8)
            self.shape = self.img.shape
            self.img_path = path
            self.process()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def process(self):
        for w in self.result_area.winfo_children():
            w.destroy()
        self.progress.set(0)
        self.update()

        h, w, c = self.shape
        raw_kb = h * w * c // 1024
        orig_kb = os.path.getsize(self.img_path) // 1024
        os.makedirs("output", exist_ok=True)

        # RLE
        self.progress.set(0.3)
        self.update()
        start = time.time()
        rle_data, _ = self.compressors["RLE"].encode(self.img)
        rle_time = time.time() - start
        rle_compressed_kb = len(rle_data) // 1024  # Kích thước dữ liệu NÉN
        rle_ratio = round(rle_compressed_kb / max(raw_kb, 1), 3)
        temp_rle = f"output/temp_{uuid.uuid4().hex}.rle"
        self.compressors["RLE"].save_file(temp_rle, rle_data, None, self.shape)
        rle_file_kb = os.path.getsize(temp_rle) // 1024

        # Huffman
        self.progress.set(0.7)
        self.update()
        start = time.time()
        huff_data, meta = self.compressors["Huffman"].encode(self.img)
        huff_time = time.time() - start
        huff_compressed_kb = len(huff_data) // 1024  # Kích thước dữ liệu NÉN
        huff_ratio = round(huff_compressed_kb / max(raw_kb, 1), 3)
        temp_huff = f"output/temp_{uuid.uuid4().hex}.huff"
        self.compressors["Huffman"].save_file(temp_huff, huff_data, meta, self.shape)
        huff_file_kb = os.path.getsize(temp_huff) // 1024

        self.progress.set(1.0)
        self.results = {
            "RLE": (rle_data, None, temp_rle, rle_file_kb, rle_compressed_kb, rle_ratio, rle_time),
            "Huffman": (huff_data, meta, temp_huff, huff_file_kb, huff_compressed_kb, huff_ratio, huff_time)
        }

        self.btn_verify.configure(state="normal")
        self.btn_export.configure(state="normal")
        self.show_results(orig_kb, raw_kb)

    def show_results(self, orig_kb, raw_kb):
        # Xóa nội dung cũ
        for widget in self.result_area.winfo_children():
            widget.destroy()

        # Giải nén lại để hiển thị
        rle_rec = self.compressors["RLE"].decode(*self.results["RLE"][:2], self.shape)
        huff_rec = self.compressors["Huffman"].decode(*self.results["Huffman"][:2], self.shape)

        # Tính toán thống kê với nhãn rõ ràng
        stats = [
            # Ảnh Gốc: raw_kb là raw_standard
            {"file": f"{orig_kb:,} KB", "raw_standard": f"{raw_kb:,} KB", "ratio": "1.0x", "time": "-"},

            # RLE: raw_kb là raw_standard, rle_compressed_kb là 'compressed'
            {
                "file": f"{self.results['RLE'][3]:,} KB",
                "compressed": f"{self.results['RLE'][4]:,} KB",
                "raw_standard": f"{raw_kb:,} KB",
                "ratio": f"{self.results['RLE'][5]}x",
                "time": f"{self.results['RLE'][6]:.3f}s"
            },

            # Huffman: raw_kb là raw_standard, huff_compressed_kb là 'compressed'
            {
                "file": f"{self.results['Huffman'][3]:,} KB",
                "compressed": f"{self.results['Huffman'][4]:,} KB",
                "raw_standard": f"{raw_kb:,} KB",
                "ratio": f"{self.results['Huffman'][5]}x",
                "time": f"{self.results['Huffman'][6]:.3f}s"
            }
        ]

        # Hiển thị 3 ảnh ngang hàng
        from gui.components import ComparisonRow
        ComparisonRow(self.result_area, self.img, rle_rec, huff_rec, stats)

        # Biểu đồ tỉ lệ nén
        fig = plt.Figure(figsize=(10, 4), facecolor="#0f172a")
        ax = fig.add_subplot(111)
        methods = ["RLE", "Huffman"]
        ratios = [self.results["RLE"][5], self.results["Huffman"][5]]
        colors = ["#22c55e" if r < 1 else "#ef4444" for r in ratios]
        bars = ax.bar(methods, ratios, color=colors, edgecolor="white", linewidth=1.5)
        ax.set_ylabel("Tỉ lệ nén", fontsize=14, color="white")
        ax.set_title("So sánh hiệu suất nén", fontsize=18, color="white", pad=20)
        ax.axhline(1, color="#f87171", linestyle="--", linewidth=2, label="Không nén")
        ax.legend()

        for bar, ratio in zip(bars, ratios):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + max(ratios) * 0.02,
                    f'{ratio}x', ha='center', va='bottom', fontweight='bold', fontsize=14, color="white")

        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        fig.patch.set_facecolor('#0f172a')
        ax.set_facecolor('#0f172a')

        canvas = FigureCanvasTkAgg(fig, self.result_area)
        canvas.get_tk_widget().pack(pady=30)
        canvas.draw()

    def verify(self):
        rle_rec = self.compressors["RLE"].decode(*self.results["RLE"][:2], self.shape)
        huff_rec = self.compressors["Huffman"].decode(*self.results["Huffman"][:2], self.shape)
        mse_rle, psnr_rle = calculate_mse_psnr(self.img, rle_rec)
        mse_huff, psnr_huff = calculate_mse_psnr(self.img, huff_rec)
        status = "HOÀN HẢO – LOSSLESS 100%" if mse_rle == 0 and mse_huff == 0 else "CÓ SAI LỆCH"
        messagebox.showinfo("Kiểm tra Lossless", f"RLE: MSE={mse_rle:.2e}, PSNR={'∞' if mse_rle==0 else f'{psnr_rle:.2f}dB'}\n"
                                                f"Huffman: MSE={mse_huff:.2e}, PSNR={'∞' if mse_huff==0 else f'{psnr_huff:.2f}dB'}\n\n{status}")

    def show_export_menu(self):
        menu = ctk.CTkToplevel(self)
        menu.title("Xuất file")
        menu.geometry("300x250")
        ctk.CTkButton(menu, text="Xuất .rle", command=lambda: self.save("RLE", ".rle")).pack(pady=10, fill="x", padx=20)
        ctk.CTkButton(menu, text="Xuất .huff", command=lambda: self.save("Huffman", ".huff")).pack(pady=10, fill="x", padx=20)
        ctk.CTkButton(menu, text="PNG từ RLE", command=lambda: self.save_png("RLE")).pack(pady=10, fill="x", padx=20)
        ctk.CTkButton(menu, text="PNG từ Huffman", command=lambda: self.save_png("Huffman")).pack(pady=10, fill="x", padx=20)

    def save(self, method, ext):
        path = filedialog.asksaveasfilename(defaultextension=ext, initialdir="output")
        if path:
            import shutil
            shutil.copy(self.results[method][2], path)
            messagebox.showinfo("Thành công", f"Đã lưu: {path}")

    def save_png(self, method):
        path = filedialog.asksaveasfilename(defaultextension=".png", initialdir="output")
        if path:
            img = self.compressors[method].decode(*self.results[method][:2], self.shape)
            Image.fromarray(img).save(path)
            messagebox.showinfo("Thành công", f"Đã lưu: {path}")