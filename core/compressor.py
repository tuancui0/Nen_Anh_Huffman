# core/compressor.py
from abc import ABC, abstractmethod
from typing import Tuple, Any
import numpy as np

class Compressor(ABC):
    @abstractmethod
    def encode(self, img: np.ndarray) -> Tuple[bytes, Any]:
        """Trả về (dữ liệu nén, metadata)"""
        pass

    @abstractmethod
    def decode(self, data: bytes, metadata: Any, shape: Tuple[int, ...]) -> np.ndarray:
        pass

    @abstractmethod
    def save_file(self, path: str, data: bytes, metadata: Any, shape: Tuple[int, ...]):
        pass

    @abstractmethod
    def load_file(self, path: str) -> np.ndarray:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass