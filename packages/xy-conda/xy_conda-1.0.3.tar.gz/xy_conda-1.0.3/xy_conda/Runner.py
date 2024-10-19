# -*- coding: UTF-8 -*-
__author__ = 'helios'
__doc__ = 'Runner'
'''
  * @File    :   Runner.py
  * @Time    :   2023/06/08 16:19:06
  * @Author  :   helios
  * @Version :   1.0
  * @Contact :   yuyang.0515@qq.com
  * @License :   (C)Copyright 2019-2023, Ship of Ocean
  * @Desc    :   None
'''
from argparse import Namespace
import os
from pathlib import Path
from datetime import datetime
from xy_argparse.ArgParse import ArgParse
from .Conda import Conda
from xy_console.utils import print_e, print_s, print_r, inputt


class Runner(ArgParse):
    conda = Conda()
    work_list = [
        "backup",
        "install",
        "install_pack",
        "load",
    ]

    def __init__(self):
        self.prog = "xy_conda"
        self.description = "conda相关工具"

    def main(self):
        self.default_parser()
        self.add_arguments()
        self.parse_arguments()
        if self.work:
            self.run_arguments()
        else:
            self.parser.print_help()

    def add_arguments(self):
        self.add_argument(
            flag="-w",
            name="--work",
            help_text="""
                工作方式:
                "backup + [name]" 备份，环境名称可选,
                "install + [url]" 安装 miniconda,
                "install_pack" 安装pack包,
                "load + [name] + [target_path] + [filepath]" 加载环境包, name:conda环境名称, target_path:目标路径, filepath:环境包文件
            """,
        )
        self.add_argument(
            flag="-n",
            name="--name",
            help_text="""
                conda环境名称 仅支持英文:
            """,
        )
        self.add_argument(
            flag="-u",
            name="--url",
            help_text="conda安装包url地址",
        )
        self.add_argument(
            flag="-t",
            name="--target_path",
            help_text="目标路径",
        )
        self.add_argument(
            flag="-f",
            name="--filepath",
            help_text="备份包路径",
        )

    @property
    def name(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.name
        return None

    @property
    def work(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.work
        return None

    @property
    def url(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.url
        return None

    @property
    def filepath(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.filepath
        return None

    @property
    def target_path(self):
        arguments = self.arguments()
        if isinstance(arguments, Namespace):
            return arguments.target_path
        return None

    def on_arguments(
        self,
        name,
        value,
        arguments=None,
    ):
        # "backup",
        # "install",
        # "install_pack",
        # "load",
        if name == "work":
            if value == "backup":
                self.backup()
                return False
            elif value == "load":
                self.load()
                return False
            elif value == "install":
                self.install()
                return False
            elif value == "install_pack":
                self.install_pack()
                return False
        return True

    def backup(self):
        name = self.name
        env_exists = self.conda.env_exists(name=name)
        if env_exists:
            print_r(f"开始备份环境 {name}...")
            ok = self.conda.backup(name=name)
            if ok:
                print_s("备份完成")
            else:
                print_e("备份失败")
        else:
            current_conda = self.conda.current_conda()
            env_exists = self.conda.env_exists(current_conda)
            if (
                current_conda
                and isinstance(current_conda, str)
                and len(current_conda) > 0
                and env_exists is True
            ):
                validate = input(f"是否备份当前环境 {current_conda} \n输入 [Y/n] \n")
                if validate == "Y":
                    ok = self.conda.backup(current_conda)
                    if ok:
                        print_s("备份完成")
                    else:
                        print_e("备份失败")
                else:
                    print_r("备份取消: 备份conda环境取消")
            else:
                print_e("备份错误: conda环境不存在 !!!")

    def load(self):
        filepath = None
        target_path = None
        name = self.name
        current_conda = self.conda.current_conda()
        current_conda_back_file = Path(f"./{current_conda}.tar.gz")
        envs_path = self.conda.envs_path()
        if isinstance(self.filepath, str) and len(self.filepath) > 0:
            filepath = Path(self.filepath)
        if isinstance(self.target_path, str) and len(self.target_path) > 0:
            target_path = Path(self.target_path)
        if not filepath or not filepath.is_file() or not filepath.exists():
            if Path(f"{name}.tar.gz").is_file() and Path(f"{name}.tar.gz").exists():
                validate = inputt(
                    f"未传入备份包文件路径 或者 备份包文件路径不存在 是否使用 ./{name}.tar.gz \n请输入 [Y/n]\n"
                )
                if validate == "Y":
                    filepath = Path(f"{name}.tar.gz")
                else:
                    print_e("加载环境取消")
                    return
            else:
                if (
                    current_conda_back_file.exists()
                    and current_conda_back_file.is_file()
                ):
                    current_validate = inputt(
                        f"未传入备份包文件路径 是否使用当前使用的conda环境同名称的备份包 {current_conda_back_file} \n请输入 [Y/n]\n"
                    )
                    if current_validate == "Y":
                        filepath = current_conda_back_file
                    else:
                        print_e("加载环境取消")
                        return
                else:
                    print_e("加载环境失败, 未传入备份包文件")
                    return
        if not target_path or not target_path.exists() or not target_path.is_dir():
            if envs_path and envs_path.exists() and envs_path.is_dir():
                target_path = envs_path.joinpath(filepath.name.split(".")[0])
            else:
                print_e("处理目标加载路径失败...")
                return
        if target_path.exists():
            target_validate = inputt(
                f"目标conda环境路径已存在, 是否备份或覆盖.默认: 备份\n其他 => 备份; 1 => 覆盖;\n请输入 [0/1]\n"
            )
            if target_validate != "1":
                backup_file_path = Path(
                    f"{filepath.name.split('.')[0]}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
                )
                print_r(f"即将备份环境到 => {backup_file_path}")
                backup_validate = os.system(f"mv -f {target_path} {backup_file_path}") == 0
                if backup_validate is True:
                    print_s(f"备份完成\n继续...")
                else:
                    print_e(f"备份失败...")
                    return
            else:
                print_r(f"即将删除环境 => {target_path}")
                delete_validate = os.system(f"rm -rf {target_path}") == 0
                if delete_validate is True:
                    print_s(f"删除完成\n继续...")
                else:
                    print_e(f"删除失败...")
                    return
        else:
            if not os.access(target_path.parent, os.W_OK):
                print_e(f"目录 {target_path.parent} 没有写入权限!!!")
                return
            target_path.mkdir(
                parents=True,
                exist_ok=True,
            )
        if target_path.exists():
            ok = os.system(f"tar xvf {filepath} -C {target_path}") == 0
            if ok is True:
                print_s(f"加载环境完成... => {target_path}")
            else:
                print_e("加载环境失败...")
        else:
            if not os.access(target_path.parent, os.W_OK):
                print_e(f"目录 {target_path.parent} 没有写入权限!!!")
                return
            target_path.mkdir(
                parents=True,
                exist_ok=True,
            )
            ok = os.system(f"tar xvf {filepath} -C {target_path}") == 0
            if ok is True:
                print_s(f"加载环境完成... => {target_path}")
            else:
                print_e("加载环境失败...")

    def install(self):
        ok = self.conda.install()
        if ok:
            print_s("安装完成")
        else:
            print_e("安装失败")

    def install_pack(self):
        ok = self.conda.install_pack()
        if ok:
            print_s("安装完成")
        else:
            print_e("安装失败")
