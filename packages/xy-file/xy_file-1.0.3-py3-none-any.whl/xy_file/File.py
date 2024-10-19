# -*- coding: UTF-8 -*-
__author__ = "helios"
"""
  * @File    :   File.py
  * @Time    :   2023/04/22 19:25:26
  * @Author  :   余洋 
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, 希洋 (Ship of Ocean)
  * @Desc    :   None
"""
import os
import re
import logging
from pathlib import Path
import shutil


from .Filter import FileTypeFilter


class File:
    @staticmethod
    def clean(
        keyword: str | None,
        cwd: Path | str | None,
        glob_keyword: str | None,
        file_type_filter: int | str = FileTypeFilter.ANY.value,
        verbose: bool = False,
        auto_cwd: bool = True,
        ignore_hidden_files: bool = True,
        should_delete_function=None,
        log_info=print,
        log_error=print,
        log_success=print,
    ):
        if not log_info or not callable(log_info):
            log_info = print
        if not cwd:
            if auto_cwd:
                cwd = Path.cwd().resolve()
            else:
                raise FileNotFoundError("请传入工作目录路径，或者设置为默认当前所在目录路径为工作目录")
        if not os.access(cwd, os.W_OK):
            raise PermissionError(f"当前目录({cwd})没有写入权限")
        if not keyword and not glob_keyword:
            raise ValueError("请传入关键字(-g/-k)进行过滤, -k支持正则表达式, 使用正则表达式搜索功能")
        if isinstance(cwd, str):
            cwd = Path(cwd)
        if not isinstance(file_type_filter, FileTypeFilter):
            file_type_filter = FileTypeFilter.parse(file_type_filter)
        file_path_list = []
        invalidate_file_path_list = []
        work_glob = cwd.rglob(glob_keyword) if isinstance(glob_keyword, str) else []
        for file_path in work_glob:
            matched = False
            if keyword:
                try:
                    match_object = re.search(
                        r"{keyword}".format(keyword=keyword), str(file_path), re.M
                    )
                    matched = match_object != None
                except Exception as exception:
                    raise ValueError(f"正则表达式匹配失败 => {exception}")
            else:
                matched = True
            if matched:
                ok = file_type_filter.validate(file_path)
                if ignore_hidden_files:
                    hidden_file_part = [
                        part for part in file_path.parts if part.startswith(".")
                    ]
                    ok = not hidden_file_part or len(hidden_file_part) == 0
                if ok and file_path.exists():
                    file_path_list.append(str(file_path))
                else:
                    invalidate_file_path_list.append(str(file_path))
        if file_path_list:
            for a_file_path in file_path_list:
                a_file_path = Path(a_file_path)
                file_type = "文件"
                if a_file_path.is_dir():
                    file_type = "目录"
                elif a_file_path.is_symlink():
                    file_type = "软链接"
                elif a_file_path.stat().st_nlink == 2:
                    file_type = "硬连接"
                elif a_file_path.is_socket():
                    file_type = "Socket"
                elif a_file_path.is_char_device():
                    file_type = "字符设备(char_device)"
                elif a_file_path.is_block_device():
                    file_type = "块设备(block_device)"
                elif a_file_path.is_fifo():
                    file_type = "管道"
                else:
                    file_type = "文件"
                msg = f"将要删除... => [{file_type}] {a_file_path}"
                log_info(msg)
            if (
                should_delete_function
                and callable(should_delete_function)
                and should_delete_function(file_path_list, invalidate_file_path_list)
            ):
                log_info("删除开始...")
                if not verbose:
                    log_info("正在删除...")
                success_file_path_list = []
                fail_file_path_list = []
                for file_path in file_path_list:
                    a_file_path = Path(file_path)
                    try:
                        if a_file_path.exists():
                            if verbose:
                                file_type = "文件"
                                if a_file_path.is_dir():
                                    file_type = "目录"
                                elif a_file_path.is_symlink():
                                    file_type = "软链接"
                                elif a_file_path.stat().st_nlink == 2:
                                    file_type = "硬连接"
                                elif a_file_path.is_socket():
                                    file_type = "Socket"
                                elif a_file_path.is_char_device():
                                    file_type = "字符设备(char_device)"
                                elif a_file_path.is_block_device():
                                    file_type = "块设备(block_device)"
                                elif a_file_path.is_fifo():
                                    file_type = "管道"
                                else:
                                    file_type = "文件"
                                log_info(f"正在删除... => [{file_type}] {file_path} ")
                            if a_file_path.is_dir():
                                shutil.rmtree(a_file_path)
                            else:
                                a_file_path.unlink()
                            success_file_path_list.append(str(a_file_path))
                    except:
                        fail_file_path_list.append(str(a_file_path))
                if not fail_file_path_list:
                    log_success("全部删除完成 !!!")
                else:
                    for a_file_path in fail_file_path_list:
                        a_file_path = Path(a_file_path)
                        if not a_file_path.exists():
                            continue
                        file_type = "文件"
                        if a_file_path.is_dir():
                            file_type = "目录"
                        elif a_file_path.is_symlink():
                            file_type = "软链接"
                        elif a_file_path.stat().st_nlink == 2:
                            file_type = "硬连接"
                        elif a_file_path.is_socket():
                            file_type = "Socket"
                        elif a_file_path.is_char_device():
                            file_type = "字符设备(char_device)"
                        elif a_file_path.is_block_device():
                            file_type = "块设备(block_device)"
                        elif a_file_path.is_fifo():
                            file_type = "管道"
                        else:
                            file_type = "文件"
                        msg = f"还未删除... => [{file_type}] {a_file_path}"
                        log_info(msg)
                    log_success(
                        f"已成功删除 ({len(file_path_list) - len(fail_file_path_list)}) 个文件或目录!!!"
                    )
                    log_info("还剩下以上文件或目录未删除: ==>")
            else:
                log_error("取消删除...")
        else:
            log_error("当前目录下暂无符合规则的文件或目录待清理")

    @staticmethod
    def touch(file_path: Path | str | None) -> Path | None:
        if not file_path:
            return None

        if isinstance(file_path, str):
            file_path = Path(file_path)

        if file_path.exists():
            if file_path.exists():
                return file_path
            return None

        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()
            return file_path.resolve()
        except Exception as exception:
            logging.exception(exception)
            return None
