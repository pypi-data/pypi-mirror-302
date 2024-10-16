from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Wrapper[T]:
    content: T


def add(value: Wrapper[Sequence[int]]):
    return sum(value.content)


# Fine, no error
add(Wrapper((1, 2, 3)))

# error
x = Wrapper((1, 2, 3))
add(x)
