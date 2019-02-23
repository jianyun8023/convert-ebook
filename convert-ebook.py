#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os
import platform
import shutil
import subprocess
import sys
import tempfile

import lib.kindleunpack as kindleunpack
from lib.mobi_header import MobiHeader
from lib.mobi_sectioner import Sectionizer

file_source = "/Users/zhaojianyun/workspace/"
tmp_dir = os.path.join(tempfile.gettempdir(), "convert_ebook")


def kindle_gen_bin():
    system_name = platform.system()
    if system_name == "Windows":
        return os.path.abspath("lib/kindlegen/kindlegen.exe")
    elif system_name == "Linux":
        return os.path.abspath("lib/kindlegen/kindlegen-linux")
    elif system_name == "Darwin":
        return os.path.abspath("lib/kindlegen/kindlegen-macos")
    else:
        print("不支持的操作系统")


def run_bash(command):
    print(command)
    return subprocess.call(command, shell=True)


def file_del(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            file_del(c_path)
        else:
            os.remove(c_path)


def file_copy(from_file, to_file):
    print("拷贝文件[%s]到[%s]" % (from_file, to_file))
    shutil.copy(from_file, to_file)


def isKF8(file):
    sect = Sectionizer(file)
    if sect.ident != b'BOOKMOBI' and sect.ident != b'TEXtREAd':
        return False

    mh = MobiHeader(sect, 0)
    return mh.isK8()


def unpack_as_azw3(filepath, output_dir):
    kindleunpack.main(["-i", "-s", filepath, output_dir])


def find_suffix(dir, suffix):
    for name in os.listdir(dir):
        path_join = os.path.join(dir, name)
        if os.path.isdir(path_join):
            find_suffix(path_join, suffix)
        elif name.endswith(suffix):
            return path_join


def check_file(file):
    if not os.path.exists(file):
        print("文件[%s]不存在" % file)
        return False
    if not isKF8(file):
        print("文件[%s]不是mobi8的格式" % file)
        return False
    return True


def convert_kf8_to_epub(file_path, tmp):
    unpack_as_azw3(file_path, tmp)
    mobi8_dir = os.path.join(tmp, "mobi8")
    if not os.path.exists(mobi8_dir):
        print("转换失败！")
        return

    return find_suffix(mobi8_dir, ".epub")


def convert_epub_to_mobi(file_path, tmp):
    exit_code = run_bash("%s -dont_append_source \"%s\"" % (kindle_gen_bin(), file_path))
    if exit_code != 0:
        return
    return find_suffix(os.path.abspath(os.path.join(file_path, os.path.pardir)), ".mobi")


def convert(file_path, tmp):
    if os.path.exists(tmp):
        # file_del(tmp)
        shutil.rmtree(tmp_dir)
    else:
        os.mkdir(tmp)
    if not check_file(file_path):
        return

    print("转换[%s]到epub" % file_path)
    epub_file = convert_kf8_to_epub(file_path, tmp)

    is_azw3 = str(file_path).lower().endswith(".azw3")

    file_source_suffix = ".azw3" if is_azw3 else file_path[file_path.rfind("."):]
    mobi_file = None
    if epub_file and is_azw3:
        print("转换epub到mobi")
        mobi_file = convert_epub_to_mobi(epub_file, tmp)

    print(epub_file)
    print(mobi_file)
    if epub_file:
        file_copy(epub_file, file_path.replace(file_source_suffix, ".epub"))
    if mobi_file:
        file_copy(mobi_file, file_path.replace(file_source_suffix, ".mobi"))


def list_file(path, filter, call_back):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isdir(file_path):
            list_file(file_path, filter, call_back)
        elif filter(filename):
            print("找到文件[%s]" % file_path)
            call_back(file_path)


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print("请输入扫描路径")
        exit(1)
    file_source = sys.argv[1]

    print("扫描文件路径" + file_source)

    # print(tmp_dir)
    fun = lambda file_path: convert(os.path.abspath(file_path), os.path.abspath(tmp_dir))
    filter = lambda filename: filename.endswith(".azw3")

    list_file(file_source, filter, fun)
    # convert(os.path.abspath(file_source), os.path.abspath(tmp_dir))
