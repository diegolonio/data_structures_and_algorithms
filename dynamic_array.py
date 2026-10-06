import ctypes
from typing import Any


class DynamicArray():
    def __init__(self, capacity: int = 10) -> None:
        self._n: int = 0
        self._capacity: int = capacity
        self._array: ctypes.Array[Any] = self._make_array(self._capacity)

    def __len__(self) -> int:
        return self._n

    def __getitem__(self, index) -> Any:
        if not 0 <= index < self._n:
            raise IndexError("Invalid index.")

        return self._array[index]

    def _resize(self, new_capacity: int) -> None:
        new_array: ctypes.Array[Any] = self._make_array(new_capacity)

        for index in range(self._n):
            new_array[index] = self._array[index]

        self._array = new_array
        self._capacity = new_capacity

    @staticmethod
    def _make_array(capacity: int) -> ctypes.Array[Any]:
        return (capacity * ctypes.py_object)()

    def append(self, item: Any) -> None:
        if self._n == self._capacity:
            self._resize(2 * self._capacity)

        self._array[self._n] = item
        self._n += 1

    def remove(self, item: Any) -> None:
        for index1 in range(self._n):
            if self._array[index1] == item:
                for index2 in range(index1, self._n - 1):
                    self._array[index2] = self._array[index2 + 1]

                self._array[self._n - 1] = None
                self._n -= 1

                if self._capacity > 10 and self._n <= (self._capacity // 4):
                    self._resize(self._capacity // 2)

                return None

        raise ValueError("Value not found.")
