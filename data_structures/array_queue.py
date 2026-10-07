from data_structures.exceptions import Empty


class ArrayQueue[T]:
    DEFAULT_CAPACITY = 10

    def __init__(self) -> None:
        self._data: list[T|None] = [None] * ArrayQueue.DEFAULT_CAPACITY
        self._size: int = 0
        self._front: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def first(self) -> T:
        if self.is_empty():
            raise Empty("Queue is empty.")
        return self._data[self._front]

    def dequeue(self) -> T:
        if self.is_empty():
            raise Empty("Queue is empty.")

        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1

        if len(self._data) > ArrayQueue.DEFAULT_CAPACITY and 0 < self._size < len(self._data) // 4:
            self._resize(len(self._data) // 2)

        return answer

    def enqueue(self, new_item: T) -> None:
        if self._size == len(self._data):
            self._resize(2 * len(self._data))

        available_place = (self._front + self._size) % len(self._data)
        self._data[available_place] = new_item
        self._size += 1

    def _resize(self, capacity: int) -> None:
        old = self._data
        self._data = [None] * capacity

        walker = self._front

        for k in range(self._size):
            self._data[k] = old[walker]
            walker = (walker + 1) % len(old)

        self._front = 0
