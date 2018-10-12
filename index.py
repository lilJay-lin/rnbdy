from baiduyunpan import PCS
from cmd import Cmd
import json
import os
import sys
import re

f = open('account',encoding='utf-8',mode='r')
data = f.read()
f.closed
user = data.split('\n')
pcs = PCS(user[0], user[1])

help = '请输入命令：\n replace 替换的文件夹路径 替换的文件名 需要在文件名尾部添加的字符串\n format 格式化的文件夹路径'

class Client(Cmd):
    prompt = 'fun>'
    intro = '百度云盘文件名替换工具 \n' + help

    def __init__(self):
        self.renamelist = []
        self.renamedir = []
        Cmd.__init__(self)

    def do_replace(self, arg):
        self.renamelist = []
        self.renamedir = []
        args = arg.split()
        if len(args) < 3:
            print('参数缺失： replace \'替换的文件夹路径\' 替换的文件名 需要在文件名尾部添加的字符串')
        else:
            print('正在替换请稍后....')
            self.get_rename_list(args[0], args[1], args[2])
            self._rename()
            print('替换完成')

    def do_format(self, arg):
        self.renamedir = []
        args = arg.split()
        if len(args) < 1:
            print('参数缺失： format \'格式化文件夹路径\'')
        else:
            print('正在格式化....')
            self._format_dir(args[0])
            self._rename()
            print('格式化完成')

    def _rename(self):
        list = []
        if len(self.renamelist) > 0:
            for temp in self.renamelist:
                list.append(temp)
                if len(list) == 100:
                    pcs.rename(list)
                    list = []
        if len(list) > 0:
            pcs.rename(list)
        list = []
        if len(self.renamedir) > 0:
            for temp in self.renamedir:
                list.append(temp)
                if len(list) == 100:
                    pcs.rename(list)
                    list = []
        if len(list) > 0:
            pcs.rename(list)

    def do_exit(self, arg):
        print('Bye!')
        return True  # 返回True，直接输入exit命令将会退出

    # def preloop(self):
    #     print
    #     "print this line before entering the loop"

    # def postloop(self):
    #     # print 'Bye!'
    #     print
    #     "print this line after leaving the loop"
    #
    # def precmd(self, line):
    #     print
    #     "print this line before do a command"
    #     return Cmd.precmd(self, line)
    #
    # def postcmd(self, stop, line):
    #     print
    #     "print this line after do a command"
    #     return Cmd.postcmd(self, stop, line)

    def emptyline(self):
        print(help)

    def default(self, line):
        print(help)

    def get_rename_list(self, path, reStr, addStr):
        response = pcs.list_files(path)
        searchlist = response.json()
        if len(searchlist) > 0:
            for file in searchlist.get('list'):
                if file.get('isdir') == 1:
                    if file.get('server_filename').find(reStr) != -1:
                        name = file.get('server_filename').replace(reStr, addStr)
                        self.renamedir.append((file.get('path'), name))
                    self.get_rename_list(file.get('path'), reStr, addStr)
                elif file.get('server_filename').find(addStr) == -1 and file.get('server_filename').find(reStr) == -1:
                    name = file.get('server_filename').partition('.')
                    self.renamelist.append((file.get('path'), name[0] + '【公众号：' + addStr + '分享】' + name[1] + name[2]))
                elif file.get('server_filename').find(reStr) != -1:
                    name = file.get('server_filename').replace(reStr, addStr)
                    self.renamelist.append((file.get('path'), name))
                    #     # name = file.get('server_filename').partition('.')
                    #     # self.renamelist.append((file.get('path'), name[0] + addStr + name[1] + name[2]))
                    #     name = file.get('server_filename').replace(reStr, addStr)
                    #     self.renamelist.append((file.get('path'), name))
                    #     # print(renamelist)
        return

    def _format_dir(self, path):
        response = pcs.list_files(path)
        searchlist = response.json()
        for file in searchlist.get('list'):
            if file.get('isdir') == 1:
                name = file.get('server_filename')
                name = re.sub(r'\s+', '', name)
                name = re.sub(r'[a-zA-Z0-9\s]+', '', name)
                self.renamedir.append((file.get('path'), name))


if __name__ == '__main__':
    try:
        os.system('cls')
        client = Client()
        client.cmdloop()
    except:
        exit()