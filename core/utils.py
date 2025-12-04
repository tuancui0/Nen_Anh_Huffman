# core/utils.py
import numpy as np

def calculate_mse_psnr(orig: np.ndarray, rec: np.ndarray):
    M = orig.shape[0] * orig.shape[1]
    N = orig.shape[2]
    se = (orig.astype(float) - rec.astype(float)) ** 2
    mse = np.sum(se) / (M * N)
    psnr = float('inf') if mse == 0 else 10 * np.log10((255**2) / mse)
    return mse, psnr

def format_bytes(size: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"