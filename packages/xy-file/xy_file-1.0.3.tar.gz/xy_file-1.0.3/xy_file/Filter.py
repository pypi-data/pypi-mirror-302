# -*- coding: UTF-8 -*-
__author__ = "helios"
__doc__ = "Filter"
"""
  * @File    :   Filter.py
  * @Time    :   2023/04/23 21:53:04
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, 希洋 (Ship of Ocean)
  * @Desc    :   None
"""

from enum import IntEnum
from pathlib import Path


class FileTypeFilter(IntEnum):
    ANY = 0
    FILE = 1
    DIR = 2
    SYMLINK = 3
    HARDLINK = 4
    SOCKET = 5
    CHAR_DEVICE = 6
    BLOCK_DEVICE = 7
    FIFO = 8

    @classmethod
    def parse(cls, file_type_filter: str | int | None):
        if not file_type_filter:
            return FileTypeFilter.ANY

        names = [member for member in cls if member.name.upper() == file_type_filter]
        if not names and len(names) > 0:
            return names[0]

        values = [member for member in cls if member.value == file_type_filter]
        if not values and len(values) > 0:
            return values[0]

        return FileTypeFilter.ANY

    def validate(self, path: Path) -> bool:
        if not path or not path.exists():
            return False

        match self:
            case FileTypeFilter.ANY:
                return True
            case FileTypeFilter.FILE:
                return path.is_file()
            case FileTypeFilter.DIR:
                return path.is_dir()
            case FileTypeFilter.SYMLINK:
                return path.is_symlink()
            case FileTypeFilter.HARDLINK:
                return path.stat().st_nlink == 2
            case FileTypeFilter.SOCKET:
                return path.is_socket()
            case FileTypeFilter.CHAR_DEVICE:
                return path.is_char_device()
            case FileTypeFilter.BLOCK_DEVICE:
                return path.is_block_device()
            case FileTypeFilter.FIFO:
                return path.is_fifo()
            case _:
                return True
