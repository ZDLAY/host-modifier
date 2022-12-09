import os

from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader

VERSION = '1.0.2'

# author 我是指针*
# email chinadlay@163.com
# 制作时间： 2022-04-14
# 更新时间： 2022-12-09

# 原始host
default = '''# Copyright (c) 1993-2009 Microsoft Corp.

#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host
# localhost name resolution is handled within DNS itself.
# 127.0.0.1       localhost
# ::1             localhost
# To allow the same kube context to work on the host and the container:
127.0.0.1 kubernetes.docker.internal
# End of section
'''


# 主类
class Win_Host:
    def __init__(self):
        # 加载界面
        self.ui = QUiLoader().load('main.ui')

        # 保存模板
        self.ui.save_format.clicked.connect(self.save2format)

        # 模板到最终
        self.ui.now.clicked.connect(self.format2now)

        # 复制到host
        self.ui.btn_host.clicked.connect(self.copy2host)

        # 模板路径
        self.template_path = os.environ['USERPROFILE'] + '\\host.kyz'

        # 设置模板
        try:
            file = open(self.template_path, 'r')
            self.host = file.read()
            self.ui.text_format.setText(self.host)
            file.close()
        except FileNotFoundError:
            print("写入模板")
            file = open(self.template_path, 'w')
            file.write(default)
            self.host = default
            file.close()

    # 模板到最终
    def format2now(self):
        ip = self.ui.ip_edit.text()
        now = self.host.replace('{}', ip)
        self.ui.text_now.setText(now)

    # 保存模板
    def save2format(self):
        hosts = self.ui.text_format.toPlainText()
        file = open(self.template_path, 'w')
        file.write(hosts)
        file.close()
        print("保存成功")
        QMessageBox.information(self.ui, "提示", "保存成功")

    # 复制到host
    def copy2host(self):
        hosts = self.ui.text_now.toPlainText()
        file = open(r'hosts.txt', 'w')
        file.write(hosts)
        file.close()
        os.system(r'copy hosts.txt C:\Windows\System32\drivers\etc\hosts')
        os.system(r'ipconfig /flushdns')
        print("复制回去成功")
        os.system(r'copy hosts.txt C:\Windows\System32\drivers\etc\hosts')
        os.system(r'ipconfig /flushdns')
        print("复制回去成功")
        os.system('del hosts.txt')


if __name__ == '__main__':
    # 欢迎大家使用这款工具

    print("欢迎使用hosts修改器，当前版本：{}".format(VERSION, {}))

    print("正在判断权限是否设置正确")

    try:
        # 判断权限
        host = open(r'C:\Windows\System32\drivers\etc\hosts', mode='r+')
        host.close()

        print("获取权限成功")

        print("程序开始运行")

        app = QApplication([])

        WinHostMian = Win_Host()

        WinHostMian.ui.show()
        app.exec_()
    except AttributeError:
        print("获取权限失败")
        exit()
