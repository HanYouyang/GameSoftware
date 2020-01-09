import sys
# 不能增加__init__.py在文件树中 得修改下面main里面的序列文件位置
# 不能安装brew的python3 用-v查看时候是在usr/bin里面才行
# pip3 install 每次换文件夹都得使用
# sudo python3 -m pip uninstall pip
# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# sudo python get-pip.py 必须得全局外网
# 不用上面这一通也得知道自己写的test里面是什么因为自己不然根本不知道运行没运行
# 目前出现no module就全部删除不管中

# 必须安装xcode
# from . import x16asm
import time
import os
import datetime


from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class AutoTest(PatternMatchingEventHandler):
    patterns = ["*.py"]

    def process(self, event):
        print('auto test', os.getcwd())
        print(datetime.datetime.now().strftime("%Y/%m/%d %I:%M %p"))
        os.system('nosetests')

    def on_modified(self, event):
        self.process(event)


def main():
    path = '../axe8'
    observer = Observer()
    observer.schedule(AutoTest(), path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


if __name__ == '__main__':
    main()
