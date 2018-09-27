from baiduyunpan import PCS
from cmd import Cmd
import json
import os
import sys

f = open('account',encoding='utf-8',mode='r')
data = f.read()
f.closed
user = data.split('\n')
pcs = PCS(user[0], user[1])


class Client(Cmd):
    prompt = 'fun>'
    intro = '百度云盘文件名替换工具 \n请输入命令： replace 替换的文件夹路径 需要在文件名尾部添加的字符串\n输入exit退出'

    def __init__(self):
        self.renamelist = []
        Cmd.__init__(self)

    def do_replace(self, arg):
        self.renamelist = []
        args = arg.split()
        if len(args) < 2:
            print('参数缺失： replace \'替换的文件夹路径\' \'需要在文件名尾部添加的字符串\'')
        else:
            print('正在替换请稍后....')
            self.get_rename_list(args[0], args[1])
            if len(self.renamelist) > 0:
                pcs.rename(self.renamelist)
            print('替换完成')

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
        print('请输入命令： replace 替换的文件夹路径 需要在文件名尾部添加的字符串')

    def default(self, line):
        print('请输入命令： replace 替换的文件夹路径 需要在文件名尾部添加的字符串')

    def get_rename_list(self, path, addStr):
        response = pcs.list_files(path)
        searchlist = response.json()
        for file in searchlist.get('list'):
            if file.get('isdir') == 1:
                self.get_rename_list(file.get('path'), addStr)
            elif file.get('server_filename').find(addStr) == -1:
                name = file.get('server_filename').partition('.')
                self.renamelist.append((file.get('path'), name[0] + addStr + name[1] + name[2]))
                # print(renamelist)
        return


if __name__ == '__main__':
    try:
        os.system('cls')
        client = Client()
        client.cmdloop()
    except:
        exit()