# -*- coding:utf-8 -*-
from fontTools.ttLib import TTFont
from fontTools.pens.areaPen import AreaPen
from tqdm import tqdm
import os

with open('unfont-chars.txt', 'w') as f:
    pass


# 通过字符图形的笔画比例来判断字符是否可视化,遍历所有unicode字符
# require freetype-py,matplotlib

def display(char, GlyphSet, Cmap, font):
    pen = AreaPen()
    glyph_set = GlyphSet
    glyph = glyph_set[Cmap[ord(char)]]
    width, ascender, descender = glyph.width, font['OS/2'].usWinAscent, -font['OS/2'].usWinDescent
    height = ascender - descender
    if width == 0:
        width = 500
    if height == 0:
        height = 1000
    try:
        glyph.draw(pen)
        blackarea = abs(pen.value)
        total_area = width * height
        if total_area == 0:
            rat = 0
        else:
            rat = blackarea / total_area
    except:
        rat = -1
    return rat


def findChar(char, font_path, fontnum=-1):
    font = TTFont(font_path, fontNumber=fontnum)
    if font.getBestCmap() and ord(char) in font.getBestCmap().keys():
        return True
    else:
        return False

def font_dict(file_list):
    res = {}
    for filename in file_list:
        file = filename
        if str(file).endswith(".ttf"):
            fontnum = -1
        elif str(file).endswith(".ttc"):
            fontnum = 0
        else:
            continue
        font = TTFont(file, fontNumber=fontnum)
        if file not in res.keys():
            res[file] = {}
            res[file]["font"] = font
            res[file]["Cmap"] = font.getBestCmap()
            res[file]["GlyphSet"] = font.getGlyphSet()
    return res

def create_test_file(char,i):
    character = "%s" % hex(ord(chr(i)))[2:].zfill(4)
    filename = '%s-A%sB' % (character, char)
    if not os.path.exists("./samples"):
        # 如果目录不存在，则创建目录
        os.makedirs("./samples")
    try:
        with open('./samples/%s.txt'%filename, 'a') as f:
            f.write()
    except:
        pass

def invisible_check(char):
    visible = []
    invisible = []
    found_fonts = []
    for key in fontDb.keys():
        cmap = fontDb[key]["Cmap"]
        if cmap and ord(char) in cmap.keys():
            found_fonts.append(key)

    if len(found_fonts) > 0:
        ratlist = []
        for fontfile in found_fonts:
            rat = display(char, fontDb[fontfile]["GlyphSet"], fontDb[fontfile]["Cmap"], fontDb[fontfile]["font"])
            ratlist.append(rat)
        if min(ratlist) == 0:
            invisible.append(r"\u%s" % hex(ord(char))[2:].zfill(4))
        else:
            visible.append(char)
    else:
        invisible.append(r"\u%s" % hex(ord(char))[2:].zfill(4))
    if len(invisible) > 0:
        # print("[!]在所选字体下的不可见字符：%s" % (",".join(invisible)))
        return char
    return False

# 指定字体文件路径
font_dir = [
    r'C:\Windows\Fonts\segoeui.ttf',  # windows系统默认
    # r'C:\Windows\Fonts\arial.ttf',  # arial,常用字体
    # r'C:\Windows\Fonts\msyh.ttc',  # 微软雅黑
    # r'C:\Windows\Fonts\msjh.ttc',  # 微软正黑
    # r'C:\Windows\Fonts\malgun.ttf',  # 韩语
    # r'C:\Windows\Fonts\msgothic.ttc',  # 日语
    # r'C:\Windows\Fonts\LeelawUI.ttf',  # 泰语
]

print("创建字体库索引...")
filelist = font_dir
fontDb = font_dict(filelist)  # 创建字体库索引
print("检测的目标字体：")
for i in font_dir:
    print(i)
res = []
targets = range(0x10000)
for i in tqdm(targets, desc="正在检测", leave=False):
    char = invisible_check(chr(i))
    output = "\\u%s" % hex(ord(chr(i)))[2:].zfill(4)
    if char:
        res.append(output)
        create_test_file(char,i)
        with open('unfont-chars.txt', 'a') as f:
            f.write(str(output) + "\n")
    else:
        print("\r%s:%s" % (output, chr(i)))
print("Find %i chars" % len(res))
