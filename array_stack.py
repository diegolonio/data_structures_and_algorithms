from exceptions import Empty


class ArrayStack:
    def __init__(self) -> None:
        self._data: list[int] = []

    def __len__(self) -> int:
        return len(self._data)

    def __str__(self) -> str:
        if self.is_empty():
            return "Stack is empty"
        return str(self._data)

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def push(self, item: int) -> None:
        self._data.append(item)

    def top(self) -> int:
        if self.is_empty():
            raise Empty("Stack is empty.")
        return self._data[-1]

    def pop(self) -> int:
        if self.is_empty():
            raise Empty("Stack is empty.")
        return self._data.pop()
