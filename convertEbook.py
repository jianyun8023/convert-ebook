#! /usr/bin/python
# -*- coding: UTF-8 -*-
import json
import os
import shutil
import uuid

import threadpool

import lib.kindleunpack as kindleunpack
from lib.mobi_header import MobiHeader
from lib.mobi_sectioner import Sectionizer
from utils import print_log, run_bash


class Config:
    source = ""
    epub_version = ""
    kindlegen_bin = ""
    bundle_dir = ""
    tmp_dir = ""
    thread_count = 1

    def __str__(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


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


def unpack_as_azw3(filepath, output_dir, config):
    kindleunpack.print = lambda str: str
    kindleunpack.main(["-i", "-s", "--epub_version=" + config.epub_version, filepath, output_dir])


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


def convert_kf8_to_epub(file_path, tmp, config):
    unpack_as_azw3(file_path, tmp, config)
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


def convert_epub_to_mobi(file_path, config: Config):
    exit_code = run_bash("%s -dont_append_source \"%s\"" % (config.kindlegen_bin, file_path))
    file = find_suffix(os.path.abspath(os.path.join(file_path, os.path.pardir)), ".mobi")
    if file and os.path.exists(file):
        print_log("[success]转换到mobi成功[%s]" % file_path)
    else:
        print_log("[fail]转换到mobi失败[%s]" % file_path)
    return file


def convert(source_file, config: Config):
    if not check_file(source_file):
        return

    temp_dir_name = str(uuid.uuid1())
    temp_dir = os.path.join(config.tmp_dir, temp_dir_name)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    print_log("转换[%s]到epub" % source_file)
    epub_file = convert_kf8_to_epub(source_file, temp_dir, config)

    is_azw3 = str(source_file).lower().endswith(".azw3")

    file_source_suffix = ".azw3" if is_azw3 else source_file[source_file.rfind("."):]

    if epub_file:
        file_copy(epub_file, source_file.replace(file_source_suffix, ".epub"))

    mobi_file = None
    if epub_file and is_azw3:
        print_log("转换epub到mobi [%s]" % epub_file)
        mobi_file = convert_epub_to_mobi(epub_file, config)

    if mobi_file:
        file_copy(mobi_file, source_file.replace(file_source_suffix, ".mobi"))


def list_file(path, filter, call_back):
    if os.path.isfile(path):
        if filter(path):
            call_back(path)
        return

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isdir(file_path):
            list_file(file_path, filter, call_back)
        elif filter(filename):
            print_log("添加转换文件[%s]" % file_path)
            call_back(file_path)


def main(config: Config):
    source = config.source
    pool = threadpool.ThreadPool(config.thread_count)

    function = lambda file_path: convert(os.path.abspath(file_path), config)
    call_back = lambda file_path: pool.putRequest(threadpool.makeRequests(function, {file_path})[0])

    filter_file = lambda filename: filename.endswith(".azw3") | filename.endswith(".mobi")

    list_file(source, filter_file, call_back)
    pool.wait()
