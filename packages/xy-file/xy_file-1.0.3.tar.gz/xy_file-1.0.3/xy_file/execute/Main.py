# -*- coding: UTF-8 -*-
__author__ = "helios"
__doc__ = "Main"
"""
  * @File    :   Main.py
  * @Time    :   2023/06/10 14:06:17
  * @Author  :   余洋
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, 希洋 (Ship of Ocean)
  * @Desc    :   None
"""

import argparse
import xy_file
from xy_file.File import File
import pkg_resources
from xy_file.utils import print_e, print_s, inputt, print_r


def should_delete(
    validate_file_path_list: list[str],
) -> bool:
    command = inputt(
        f"是否删除以上共 ({len(validate_file_path_list)}) 个文件和目录，\n\n【确定】请输入[Y], 输入其他按键进行【取消】。\n\n输入[Y/n] : \n"
    )
    return command == "Y"


def main():
    desc = f"{xy_file.__name__}-{pkg_resources.get_distribution(xy_file.__name__).version}: => 文件操作程序 - v{pkg_resources.get_distribution(xy_file.__name__).version}"
    print(desc)
    parser = argparse.ArgumentParser(
        prog=xy_file.__name__,
        description=desc,
    )
    work_list = [
        "clean",  # 必须添加-n参数作为新的project_name项目名称
    ]
    parser.add_argument(
        "-w",
        "--work",
        type=str,
        help="""
            命令:
            -----clean => 清理文件或目录
        """,
        choices=work_list,
        required=True,
    )
    parser.add_argument(
        "-g",
        "--glob-keyword",
        type=str,
        help="""
        工作目录过滤匹配关键字; 
        默认: **/*, 当前目录下的全部文件和目录，
        可选，工作目录过滤关键字，使用普通命令行文件匹配，例如 *.py表示当前目录下所有py脚本""",
        required=False,
        default="**/*",
    )
    parser.add_argument(
        "-k",
        "--keyword",
        type=str,
        help="关键字; 可选; 使用正则表达式Search; re.M模式, !!! 注意: 该关键字匹配是绝对路径字符串",
        required=False,
    )
    parser.add_argument(
        "-c",
        "--cwd",
        type=str,
        help="""工作目录; 默认命令行当前目录; 当auto_cwd为False且未传入工作目录时报错""",
        required=False,
    )
    parser.add_argument(
        "-i",
        "--ignore_hidden_files",
        type=int,
        help="""是否忽略隐藏目录和文件""",
        required=False,
        default=1,
    )
    parser.add_argument(
        "-f",
        "--file-type-filter",
        help="""
                        
                        过滤器, 默认为0; 无限制,
                        !!! 若输入字符串则无大小写限制,
                        以下为过滤器对应类型:
                        任意 = [0, any],
                        文件 = [1, file],
                  目录/文件夹 = [2, dir],
                      软链接 = [3, symlink],
                      硬链接 = [4, hardlink],
                     Socket = [5, socket],
        字符设备(char device) = [6, char_device],
        块设备(block device) = [7, block_device],
                  管道(fifo) = [8, fifo],
                        
                        """,
        default=0,
        required=False,
    )
    parser.add_argument(
        "-vb",
        "--verbose",
        type=bool,
        help="是否显示工作详情; 默认为0或者False",
        required=False,
        default=False,
    )
    parser.add_argument(
        "-ac",
        "--auto-cwd",
        type=bool,
        help="是否自动设置工作目录为当前目录; 默认为True",
        default=True,
    )
    work = parser.parse_args().work
    match work:
        case "clean":
            glob_keyword = parser.parse_args().glob_keyword
            keyword = parser.parse_args().keyword
            cwd = parser.parse_args().cwd
            file_type_filter = parser.parse_args().file_type_filter
            verbose = parser.parse_args().verbose
            auto_cwd = parser.parse_args().auto_cwd
            ignore_hidden_files = parser.parse_args().ignore_hidden_files
            try:
                ignore_hidden_files = bool(ignore_hidden_files)
            except:
                ignore_hidden_files = True
            try:
                File.clean(
                    glob_keyword=glob_keyword,
                    keyword=keyword,
                    cwd=cwd,
                    file_type_filter=file_type_filter,
                    verbose=verbose,
                    auto_cwd=auto_cwd,
                    ignore_hidden_files=ignore_hidden_files,
                    should_delete_function=should_delete,
                    log_info=print_r,  # type: ignore
                    log_success=print_s,  # type: ignore
                    log_error=print_e,  # type: ignore
                )
            except Exception as exception:
                print_e(f"删除失败 => {str(exception)}")

        case _:
            print_e("请输入-w/--work参数 !!!")


if __name__ == "__main__":
    main()
