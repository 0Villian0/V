#! usr/bin/env python3
# coding = utf-8
# Author: 0Villian0
# Date: 6|5|2018
from PIL     import Image, ImageDraw, ImageFont
import time
import argparse
import os
import sys


def action_one(file_Path):
    if file_Path is None:
        print('请输入你要添加水印的图片路径，或者使用 -h|--help 查看帮助信息！')
        sys.exit()
    elif os.path.exists(file_Path):
        if os.path.isfile(file_Path):
            save_Path = get_savePath(file_Path)
            shui_yin(file_Path, save_Path)
        else:
            file_Paths = recursion_dir(file_Path)
            for f_P in file_Paths:
                save_Path = get_savePath(f_P)
                shui_yin(f_P, save_Path)
    else:
        print('你输入的路径   %s  不存在，请重新输入！' %file_Path)
        sys.exit()


def action_two(file_Path):
    if file_Path is None:
        print('请输入你要遍历的路径！或者 -h|--help 查看帮助信息！')
        sys.exit()
    elif os.path.isdir(file_Path):
        file_Paths = recursion_dir(file_Path)
        # print(len(file_Paths))
        file_Paths = sort_MTIME(file_Paths)
        # print(file_Paths)
        # print(len(file_Paths))
        return file_Paths
    elif os.path.isfile(file_Path):
        print('你输入的路径  %s  是一个文件不是目录，请重新输入！' %file_Path)
        sys.exit()
    else:
        print('你输入的路径   %s  不存在，请重新输入！' %file_Path)
        sys.exit()

# def sort_MTIME(file_Paths):
#         for f in file_Paths:
#             try:
#                 file_Paths.sort(key=lambda f: os.path.getmtime(f))
#             except Exception as E:
#                 print(E)
#                 file_Paths.remove(f)
#         return file_Paths
def sort_MTIME(file_Paths):
    i = 0
    while True:
        f = file_Paths[i]
        # print(i)
        try:
            file_Paths.sort(key=lambda f: os.path.getmtime(f))
        except Exception as E:
            print(E)
            file_Paths.remove(f)
        else:
            i += 1
        if i == len(file_Paths):
            return file_Paths


def shui_yin(filePath, save_Path):
    if analyze_dir(filePath)[3].lower() in ['.jpg', '.jpeg', '.png', '.bmp']:
        image = Image.open(filePath)
        w, h = image.size
        time_1 = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        font = ImageFont.truetype('C:\Windows\Fonts\simhei.ttf', 48)
        draw = ImageDraw.Draw(image)
        draw.text((4*w/5, 1*h/5), time_1, fill=(55, 55, 55), Font=font)
        image.save(save_Path, 'png')
        # image.show()
    else:
        print(filePath + '不是图片')


def mkdir_(folderpath):
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
    else:
        pass


def analyze_dir(path_):
    dirPath = os.path.dirname(path_)
    basefileName = os.path.basename(path_)
    fileName = os.path.splitext(basefileName)[0]
    extensionName = os.path.splitext(basefileName)[1]
    return dirPath, basefileName, fileName, extensionName


def get_savePath(file_Path):
    dirPath, basefileName, fileName, extensionName = analyze_dir(file_Path)
    save_dir = dirPath + '\\temp\\'
    save_Path = save_dir + basefileName
    mkdir_(save_dir)
    return save_Path


def recursion_dir(file_Path):
    file_Paths = []
    for dirpath, dirnames, filenames in os.walk(file_Path):
        for filename in filenames:
            file_Paths.append(os.path.join(dirpath, filename))
    return file_Paths


def arg_Parser():
    parse = argparse.ArgumentParser(prog='zero.py', description='%(prog)s help information！', epilog='''使用示例：
                                                                                               %(prog)s 1 -f D:\path''')
    parse.add_argument('action', choices=[1, 2, 3], type=int,  nargs='?', help=""" 脚本功能：
                                                                                  【1】在给定路径下所有图片添加时间水印！
                                                                                  【2】目录下所有文件按照修改时间排序！
                                                                                  【3】功能待定""")
    parse.add_argument('-f', '--file', type=str, nargs='?', help='-f|--file 文件路径(FILE)')
    argv = parse.parse_args()
    return argv


def main():
    argv = arg_Parser()
    # file_Path = r'D:\python\python3'
    file_Path = argv.file
    # action = 2
    action = argv.action
    if action is None:
        print('请输入你要使用的功能！或者 -h|--help 查看帮助信息！')
        sys.exit()
    elif action == 1:
        action_one(file_Path)
    elif action == 2:
        file_Paths = action_two(file_Path)
        print(file_Paths)
    else:
        print('功能【3】待定！')


if __name__ == '__main__':
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    main()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
