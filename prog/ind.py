#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional


class FileLister:
    def __init__(
        self,
        path: Path,
        show_time: bool,
        show_size: bool,
        only_dir: bool,
        max_level: int,
    ):
        self.path = path
        self.show_time = show_time
        self.show_size = show_size
        self.only_dir = only_dir
        self.max_level = max_level

    def list_files(self, level: int = 0) -> None:
        if level == self.max_level:
            return

        indent = f"{'   ' * level} "
        for item in self.path.iterdir():
            if item.is_file() and not self.only_dir:
                self.print_file_info(item, indent)
            elif item.is_dir():
                self.print_dir_info(item, indent)
                # Recursively list files in the directory
                sub_lister = FileLister(
                    item, self.show_time, self.show_size, self.only_dir, self.max_level
                )
                sub_lister.list_files(level + 1)

    def print_file_info(self, item: Path, indent: str) -> None:
        size = self.get_size(item)
        time = self.get_time(item)
        print(
            f"{indent}{item.name} {size if size is not None else ''} {time if time is not None else ''}"
        )

    def print_dir_info(self, item: Path, indent: str) -> None:
        size = self.get_size(item)
        time = self.get_time(item)
        print(
            f"{indent}{item.name}/ {size if size is not None else ''} {time if time is not None else ''}"
        )

    def get_size(self, item: Path) -> Optional[int]:
        if self.show_size:
            return item.stat().st_size
        return None

    def get_time(self, item: Path) -> Optional[datetime]:
        if self.show_time:
            return datetime.fromtimestamp(item.stat().st_mtime)
        return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Утилита для отображения дерева каталогов и файлов"
    )
    parser.add_argument("path", nargs="?", default=".", help="Путь к каталогу")
    parser.add_argument(
        "-l", "--level", default=1, type=int, help="Уровень вложенности"
    )
    parser.add_argument(
        "-d", "--dir", action="store_true", help="Показывать только директории"
    )
    parser.add_argument(
        "-s", "--showsize", action="store_true", help="Показать размер файлов"
    )
    parser.add_argument(
        "-t", "--time", action="store_true", help="Показать время изменения"
    )
    args = parser.parse_args()

    path = Path(args.path)
    if path.is_dir():
        lister = FileLister(path, args.time, args.showsize, args.dir, args.level)
        lister.list_files()
    else:
        print(f"Путь {args.path} не существует или не является каталогом")


if __name__ == "__main__":
    main()
