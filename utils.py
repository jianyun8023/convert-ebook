import os
import platform
import subprocess
import sys
import tempfile
import time


def get_tmp_dir():
    return os.path.join(tempfile.gettempdir(), "convert_ebook")


def get_bundle_dir():
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        return sys._MEIPASS
    else:
        # we are running in a normal Python environment
        return os.path.dirname(os.path.abspath(__file__))


def print_log(log):
    date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(date_time + ' ' + log)


def kindle_gen_bin(bundle_dir):
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
