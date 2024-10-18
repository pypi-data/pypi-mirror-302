# -*- coding: utf-8 -*-

from __future__ import annotations

import bz2
import glob
import gzip
import json
import lzma
import os
import pickle
from typing import TYPE_CHECKING, Any

import pytoml  # pyright: ignore[reportMissingTypeStubs]

from filefox import text

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Mapping


class BaseError(Exception):
    pass


class UnsupportedCompressionMethodError(BaseError):
    def __init__(self, *args: Any, ext: str | None = None) -> None:
        super().__init__(*args)
        self.ext = ext


class UnsupportedFileTypeError(BaseError):
    def __init__(self, *args: Any, ext: str | None = None) -> None:
        super().__init__(*args)
        self.ext = ext


class UnknownFileTypeError(BaseError):
    def __init__(
        self,
        *args: Any,
        filename: os.PathLike[str] | None = None,
    ) -> None:
        super().__init__(*args)
        self.filename = filename


_COMPRESSION = {
    ".bz2": bz2.open,
    ".gz": gzip.open,
    ".xz": lzma.open,
}


def _get_open_fn(filename: os.PathLike[str]) -> Callable[..., Any]:
    ext = os.path.splitext(filename)[1]

    return _COMPRESSION.get(ext, open)


def _wrap_reader(
    reader: Callable[..., Any],
    default_mode: str = "rt",
) -> Callable[..., Any]:
    def _wrapper(
        filename: os.PathLike[str],
        *args: Any,
        file_options: Mapping[str, Any] | None = None,
        **kwargs: Any,
    ):
        if file_options is None:
            file_options = {
                "mode": default_mode,
            }

        with _get_open_fn(filename)(filename, **file_options) as f:
            return reader(f, *args, **kwargs)

    return _wrapper


def _wrap_writer(
    writer: Callable[..., Any],
    default_mode: str = "wt",
) -> Callable[..., Any]:
    def _wrapper(
        obj: Any,
        filename: os.PathLike[str],
        *args: Any,
        file_options: Mapping[str, Any] | None = None,
        **kwargs: Any,
    ):
        if file_options is None:
            file_options = {
                "mode": default_mode,
            }

        with _get_open_fn(filename)(filename, **file_options) as f:
            writer(obj, f, *args, **kwargs)

    return _wrapper


read_json = _wrap_reader(json.load)
write_json = _wrap_writer(json.dump)
read_pickle = _wrap_reader(pickle.load, default_mode="rb")
write_pickle = _wrap_writer(pickle.dump, default_mode="wb")
read_toml = _wrap_reader(pytoml.load)  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
write_toml = _wrap_writer(pytoml.dump)  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
read_text = _wrap_reader(text.load)
write_text = _wrap_writer(text.dump)


class _Handler:
    def __init__(
        self, *, reader: Callable[..., Any], writer: Callable[..., Any]
    ) -> None:
        self.reader = reader
        self.writer = writer


_FILE_HANDLERS = {
    ".json": _Handler(reader=read_json, writer=write_json),
    ".pickle": _Handler(reader=read_pickle, writer=write_pickle),
    ".pkl": _Handler(reader=read_pickle, writer=write_pickle),
    ".toml": _Handler(reader=read_toml, writer=write_toml),
    ".txt": _Handler(reader=read_text, writer=write_text),
}


def _get_handler(filename: os.PathLike[str]) -> _Handler:
    basename, compression_ext = os.path.splitext(filename)
    if not compression_ext:
        msg = "Failed to detect file type"
        raise UnknownFileTypeError(msg, filename=filename)

    basename, file_ext = os.path.splitext(basename)
    if not file_ext and compression_ext not in _COMPRESSION:
        file_ext = compression_ext
        compression_ext = ""

    if compression_ext and compression_ext not in _COMPRESSION:
        msg = f"Unsupported compression method: {compression_ext}"
        raise UnsupportedCompressionMethodError(msg, ext=compression_ext)

    handler = _FILE_HANDLERS.get(file_ext)
    if not handler:
        msg = f"Unsupported file type: {file_ext}"
        raise UnsupportedFileTypeError(msg, ext=file_ext)

    return handler


def read(
    filename: os.PathLike[str],
    *args: Any,
    file_options: Mapping[str, Any] | None = None,
    **kwargs: Mapping[str, Any],
) -> Any:
    handler = _get_handler(filename)

    return handler.reader(filename, *args, file_options=file_options, **kwargs)


def read_dir(
    dirname: os.PathLike[str],
    *args: Any,
    file_pattern: str = "*",
    file_options: Mapping[str, Any] | None = None,
    **kwargs: Mapping[str, Any],
) -> Iterable[Any]:
    for filename in glob.iglob(os.path.join(dirname, file_pattern), recursive=True):
        ext = os.path.splitext(filename)[1]
        if ext not in _FILE_HANDLERS:
            continue

        yield read(filename, *args, file_options=file_options, **kwargs)


def write(
    obj: Any,
    filename: os.PathLike[str],
    *args: Any,
    file_options: Mapping[str, Any] | None = None,
    **kwargs: Mapping[str, Any],
) -> None:
    handler = _get_handler(filename)

    handler.writer(obj, filename, *args, file_options=file_options, **kwargs)


__all__ = [
    "read",
    "write",
    "read_json",
    "write_json",
    "read_pickle",
    "write_pickle",
    "read_toml",
    "write_toml",
    "BaseError",
    "UnsupportedCompressionMethodError",
    "UnsupportedFileTypeError",
    "UnknownFileTypeError",
]

__version__ = "0.6.0"
