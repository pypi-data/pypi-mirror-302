# -*- coding: utf-8 -*-

from collections.abc import Iterable
from typing import TextIO


def load(f: TextIO) -> str:
    return f.read()


def dump(text: str | Iterable[str], f: TextIO) -> None:
    if isinstance(text, str):
        _ = f.write(text)
    else:
        f.writelines(text)
