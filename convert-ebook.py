#! /usr/bin/python
# -*- coding: UTF-8 -*-
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from multiprocessing import cpu_count

import threadpool

import lib.kindleunpack as kindleunpack
from lib.mobi_header import MobiHeader
from lib.mobi_sectioner import Sectionizer

tmp_dir = os.path.join(tempfile.gettempdir(), "convert_ebook")

if getattr(sys, 'frozen', False):
    # we are running in a bundle
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))


def print_log(log):
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(date_time + ' ' + log)


def kindle_gen_bin():
    system_name = platform.system()
    if system_name == "Windows":
        return os.path.abspath(os.path.join(bundle_dir, "lib/kindlegen/kindlegen.exe"))
    elif system_name == "Linux":
        return os.path.abspath(os.path.join(bundle_dir, "lib/kindlegen/kindlegen-linux"))
    elif system_name == "Darwin":
        return os.path.abspath(os.path.join(bundle_dir, "lib/kindlegen/kindlegen-macos"))
    else:
        print_log("不支持的操作系统")


def run_bash(command):
    # print_log(command)
    return subprocess.call(command, shell=True, stdout=subprocess.DEVNULL)


def file_del(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            file_del(c_path)
        else:
            os.remove(c_path)


def file_copy(from_file, to_file):
    print_log("拷贝文件[%s]到[%s]" % (from_file, to_file))
    shutil.copy(from_file, to_file)


def isKF8(file):
    sect = Sectionizer(file)
    if sect.ident != b'BOOKMOBI' and sect.ident != b'TEXtREAd':
        return False

    mh = MobiHeader(sect, 0)
    return mh.isK8()


def unpack_as_azw3(filepath, output_dir):
    kindleunpack.print = lambda str: str
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
        print_log("文件[%s]不存在" % file)
        return False
    if not isKF8(file):
        print_log("文件[%s]不是mobi8的格式" % file)
        return False
    return True


def convert_kf8_to_epub(file_path, tmp):
    unpack_as_azw3(file_path, tmp)
    mobi8_dir = os.path.join(tmp, "mobi8")
    if not os.path.exists(mobi8_dir):
        print_log("[fail]解包文件失败[%s]" % file_path)
        return

    file = find_suffix(mobi8_dir, ".epub")
    if file and os.path.exists(file):
        print_log("[success]转换到epub成功[%s]" % file_path)
    else:
        print_log("[fail]转换到epub失败[%s]" % file_path)
    return file


def convert_epub_to_mobi(file_path, tmp):
    exit_code = run_bash("%s -dont_append_source \"%s\"" % (kindle_gen_bin(), file_path))
    if exit_code != 0:
        return
    file = find_suffix(os.path.abspath(os.path.join(file_path, os.path.pardir)), ".mobi")
    if file and os.path.exists(file):
        print_log("[success]转换到mobi成功[%s]" % file_path)
    else:
        print_log("[fail]转换到mobi失败[%s]" % file_path)
    return file


def convert(file_path, tmp):
    if not check_file(file_path):
        return

    temp_dir_name = str(uuid.uuid1())
    temp_dir = os.path.join(tmp, temp_dir_name)
    if os.path.exists(temp_dir):
        # file_del(tmp)
        shutil.rmtree(tmp_dir)
    os.makedirs(temp_dir)

    print_log("转换[%s]到epub" % file_path)
    epub_file = convert_kf8_to_epub(file_path, temp_dir)

    is_azw3 = str(file_path).lower().endswith(".azw3")

    file_source_suffix = ".azw3" if is_azw3 else file_path[file_path.rfind("."):]

    if epub_file:
        file_copy(epub_file, file_path.replace(file_source_suffix, ".epub"))

    mobi_file = None
    if epub_file and is_azw3:
        print_log("转换epub到mobi [%s]" % epub_file)
        mobi_file = convert_epub_to_mobi(epub_file, temp_dir)

    # print_log(epub_file)
    # print_log(mobi_file)

    if mobi_file:
        file_copy(mobi_file, file_path.replace(file_source_suffix, ".mobi"))


def list_file(path, filter, call_back):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isdir(file_path):
            list_file(file_path, filter, call_back)
        elif filter(filename):
            print_log("添加转换文件[%s]" % file_path)
            call_back(file_path)


if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print_log("请输入扫描路径")
        exit(1)
    file_source = sys.argv[1]

    print_log("扫描文件路径" + file_source)

    pool = threadpool.ThreadPool(cpu_count() * 2)

    fun = lambda file_path: convert(os.path.abspath(file_path), os.path.abspath(tmp_dir))
    call_back = lambda file_path: pool.putRequest(threadpool.makeRequests(fun, {file_path})[0])

    filter = lambda filename: filename.endswith(".azw3")

    list_file(file_source, filter, call_back)
    pool.wait()
