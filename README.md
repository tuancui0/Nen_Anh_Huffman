# Image Compression using Huffman + RLE + PSNR

Ứng dụng mô phỏng các phương pháp **nén ảnh có mất dữ liệu (lossy)** và **không mất dữ liệu (lossless)**, bao gồm:

- **RLE (Run-Length Encoding)** – mã hóa chiều dài chạy
- **Huffman Coding** – mã hóa entropy
- **PSNR** – đánh giá chất lượng ảnh tái tạo

Hệ thống giúp người dùng:
- Nén ảnh bằng nhiều phương pháp
- So sánh hiệu quả nén giữa **Huffman**, **RLE**, và **RLE thuần**
- Tính toán PSNR để đánh giá chất lượng ảnh sau giải nén
- Xem sự khác biệt về kích thước, tốc độ và chất lượng
  

## 🚀 **Tính năng chính**
- Xử lý ảnh RGB → YCbCr, nén chủ yếu trên kênh Y.
- Mã hóa dữ liệu bằng:
  - **Huffman**
  - **RLE**
  - Hoặc kết hợp **RLE** / **Huffman**
- Hiển thị thống kê:
  - Kích thước trước / sau nén
  - Tỉ lệ nén
  - Thời gian xử lý
  - PSNR
- So sánh trực tiếp các thuật toán nén ngay trong giao diện.
- Lưu và tải lại file nén tùy theo định dạng do nhóm tự thiết kế.


## 📁 **Cấu trúc thư mục**
BTL_XLA_2/
│── .venv/ # Môi trường ảo Python
│
│── core/ # Các thuật toán nén
│ ├── init.py
│ ├── compressor.py # Class chung cho compressor
│ ├── huffman.py # Bộ nén Huffman
│ ├── rle.py # Bộ nén RLE
│ ├── utils.py # Hàm tính PSNR, MSE, hàm hỗ trợ
│
│── gui/ # Giao diện ứng dụng
│ ├── init.py
│ ├── app.py # File chính GUI
│ ├── components.py # Các UI component (ComparisonRow, Viewer…)
│
│── output/ # Thư mục lưu file nén tạm & xuất
│
│── main.py #

## **Cách chạy**
Chạy file main.py
