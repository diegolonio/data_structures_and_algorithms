from typing import List, TypeVar
from abc import ABC, abstractmethod


class CreditCard:
    """A consumer credit card"""

    def __init__(self, customer: str, bank: str, account: str, limit: float) -> None:
        """Create a new credit card instance

        The initial balance is zero.

        customer: the name of the customer
        bank: the name of the bank
        account: the account identifier
        limit: credit limit (measured in dollars)
        """

        self._customer: str = customer
        self._bank: str = bank
        self._account: str = account
        self._limit: float = limit
        self._balance: float = 0.0

    @property
    def customer(self) -> str:
        """Return name of the customer"""
        return self._customer

    @property
    def bank(self) -> str:
        """Return name of the bank"""
        return self._bank

    @property
    def account(self) -> str:
        """Return the card identifying number"""
        return self._account

    @property
    def limit(self) -> float:
        """Return current credit limit"""
        return self._limit

    @property
    def balance(self) -> float:
        """Return current credit balance"""
        return self._balance

    def charge(self, price: float) -> bool:
        """Charge given price to credit card, assuming sufficient credit limit.

        Return True if charge was processed; False if charge was denied.
        """
        if price + self._balance > self._limit:
            return False
        else:
            self._balance += price
            return True

    def make_payment(self, amount: float) -> None:
        """Process customer payment that reduces balance"""
        self._balance -= amount


class PredatoryCreditCard(CreditCard):
    """An extension to the CreditCard that compounds interest and fees."""
    def __init__(self, customer: str, bank: str, account: str, limit: float, apr: float) -> None:
        """Create a new credit card instance

                The initial balance is zero.

                customer: the name of the customer
                bank: the name of the bank
                account: the account identifier
                limit: credit limit (measured in dollars)
        """
        super().__init__(customer, bank, account, limit)
        self._apr = apr

    def change(self, price: float) -> bool:
        """Charge given price to the card, assuming sufficient credit limit.

        Return True if charge was processed.
        Return False and assess $5 fee if charge is denied.
        """
        success: bool = super().charge(price)

        if not success:
            self._balance += 5

        return success

    def process_month(self):
        """ASsess monthly interest on outstanding balance."""
        if self._balance > 0:
            # if possible balance, convert APR to monthly multiplicative factor
            monthly_factor = pow(1 + self._apr, 1 / 12)
            self._balance += monthly_factor


class Vector:
    """Represent a vector in a multidimensional space."""

    def __init__(self, n: int|List[float]) -> None:
        """Create a n-dimensional vector of zeros."""

        if isinstance(n, int):
            self._coords: list = [0.0] * n
        else:
            self._coords: list = [float(x) for x in n]

    def __len__(self) -> int:
        """Return the dimension of the vector."""
        return len(self._coords)

    def __getitem__(self, j: int) -> float:
        """Return j-th coordinate of vector."""
        return self._coords[j]

    def __setitem__(self, j: int, val: float) -> None:
        """Set j-th coordinate of vector to given value."""
        self._coords[j] = float(val)

    def __add__(self, other: "Vector") -> "Vector":
        """Return sum of two vectors."""
        if len(self) != len(other):
            raise ValueError("Vector length mismatch")

        result = Vector(len(self))

        for j in range(len(self)):
            result[j] = self[j] + other[j]

        return result

    def __eq__(self, other: "Vector") -> bool:
        """Return True if vector has the same coordinates as other."""
        return self._coords == other._coords

    def __ne__(self, other: "Vector") -> bool:
        """Return True if vector differs from other."""
        return not (self == other)

    def __str__(self) -> str:
        """Produce string representation of vector."""
        return "<" + str(self._coords)[1:-1] + ">"


class SequenceIterator:
    """An iterator for any of Python's sequence types"""

    def __init__(self, sequence) -> None:
        """Create an iterator for the given sequence."""
        self._sequence = sequence # Keep a reference to the underlying data.
        self._index: int = -1 # Will increment to 0 on first call to next.

    def __next__(self) -> TypeVar:
        """Return the next element, or else raise StopIteration error."""
        self._index += 1
        if self._index < len(self._sequence):
            return self._sequence[self._index]
        else:
            raise StopIteration

    def __iter__(self) -> "SequenceIterator":
        """By convention, an iterator must return itself as an iterator."""
        return self


class Progression:
    def __init__(self, start: int = 0) -> None:
        self._current: int = start

    def _advance(self) -> None:
        self._current += 1

    def __next__(self) -> int:
        if self._current is None:
            raise StopIteration
        else:
            answer = self._current
            self._advance()
            return answer

    def __iter__(self) -> "Progression":
        return self

    def print_progression(self, n: int) -> None:
        print(" ".join(str(next(self)) for _ in range(n)))


class ArithmeticProgression(Progression):
    def __init__(self, increment: int = 1, start: int = 0) -> None:
        super().__init__(start)
        self._increment: int = increment

    def _advance(self) -> None:
        self._current += self._increment


class GeometricProgression(Progression):
    def __init__(self, base: int = 2, start: int = 1) -> None:
        super().__init__(start)
        self._base: int = base

    def _advance(self) -> None:
        self._current *= self._base


class FibonacciProgression(Progression):
    def __init__(self, first: int = 0, second: int = 1) -> None:
        super().__init__(first)
        self._previous: int = second - first

    def _advance(self) -> None:
        self._previous, self._current = self._current, self._previous + self._current


class Sequence(ABC):
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self, j):
        pass

    def __contains__(self, value: TypeVar) -> bool:
        for j in range(len(self)):
            if self[j] == value:
                return True

        return False

    def index(self, value: TypeVar) -> int:
        for j in range(len(self)):
            if self[j] == value:
                return j
        raise ValueError("Value not in Sequence")

    def count(self, value: TypeVar) -> int:
        k = 0
        for j in range(len(self)):
            if self[j] == value:
                k += 1

        return k


if __name__ == '__main__':

    wallet: list = [
        CreditCard("Diego Armando Apolonio Villegas", "BBVA", "5391 0375 9387 5309", 40000.0),
        CreditCard("Gabriela Anamyle Medina Villegas", "Banamex", "7657 6876 3909 9328", 11000.0),
        CreditCard("Alejandro Apolonio Villegas", "Banco Apócrifo", "2390 4394 3654 3409", 8000.0)
    ]

    for i in range(1, 17):
        wallet[0].charge(i)
        wallet[1].charge(i * 2)
        wallet[2].charge(i * 3)

    for c in range(3):
        print(f"Customer = {wallet[c].customer}")
        print(f"Bank = {wallet[c].bank}")
        print(f"Account = {wallet[c].account}")
        print(f"Limit = {wallet[c].limit}")
        print(f"Balance = {wallet[c].balance}")

        while wallet[c].balance > 100:
            wallet[c].make_payment(100)
            print(f"New Balance = {wallet[c].balance}")

        print("\n")


    a_vector = Vector([5, 6, 7])
    another_vector = Vector(3)

    another_vector[0] = a_vector[0]
    another_vector[1] = a_vector[1]
    another_vector[2] = a_vector[2]

    print(f"V1 = {a_vector}, V2 = {another_vector}\n")

    print(f"Addition = {a_vector + another_vector}\n")

    print(f"They are equal = {a_vector == another_vector}\n")

    print(f"They are distinct = {another_vector != a_vector}\n")

    for component in range(len(a_vector)):
        print(f"a_vector[{component}] = {a_vector[component]} | another_vector[{component}] = {another_vector[component]}\n")

    progression = Progression()
    progression.print_progression(10)

    arithmetic_progression = ArithmeticProgression(increment=2)
    arithmetic_progression.print_progression(10)

    geometric_progression = GeometricProgression(base=2)
    geometric_progression.print_progression(10)

    fibonacci = FibonacciProgression()
    fibonacci.print_progression(10)

    print(CreditCard.__dict__, "\n")

    a_list = [1, [2], 3]
    another_list = [4, [5], 6]

    a = a_list
    b = another_list

    print(f"a = {id(a)} | a_list = {id(a_list)} | a is a_list = {a is a_list}")
    print(f"b = {id(b)} | another_list = {id(another_list)} | b is another_list = {b is another_list}")

    a[1][0] = 100
    b[1][0] = 33

    print(f"a = {a} | a_list = {a_list}")
    print(f"b = {b} | another_list = {another_list}")
    print()

    # Creating a shallow copy

    from copy import copy

    a_list = [1, [2], 3]
    another_list = [4, [5], 6]

    a = copy(a_list)
    b = copy(another_list)

    print(f"a = {id(a)} | a_list = {id(a_list)} | a is a_list = {a is a_list}")
    print(f"b = {id(b)} | another_list = {id(another_list)} | b is another_list = {b is another_list}")

    a[1][0] = 100
    b[1][0] = 33

    print(f"a = {a} | a_list = {a_list}")
    print(f"b = {b} | another_list = {another_list}")
    print()

    # Creating a deep copy

    from copy import deepcopy

    a_list = [1, [2], 3]
    another_list = [4, [5], 6]

    a = deepcopy(a_list)
    b = deepcopy(another_list)

    print(f"a = {id(a)} | a_list = {id(a_list)} | a is a_list = {a is a_list}")
    print(f"b = {id(b)} | another_list = {id(another_list)} | b is another_list = {b is another_list}")

    a[1][0] = 100
    b[1][0] = 33

    print(f"a = {a} | a_list = {a_list}")
    print(f"b = {b} | another_list = {another_list}")
