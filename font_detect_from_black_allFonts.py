# -*- coding:utf-8 -*-
from fontTools.ttLib import TTFont
from fontTools.pens.areaPen import AreaPen
import os


# 通过字符图形的笔画比例来判断字符是否可视化
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

def findChar(char, font_path, fontnum=-1):
    font = TTFont(font_path, fontNumber=fontnum)
    GlyphSet = font.getGlyphSet()
    index = ord(char)
    if font.getBestCmap() and index in font.getBestCmap().keys() and font.getBestCmap()[index] in list(GlyphSet.keys()):
        return True
    else:
        return False


# 指定字体文件路径
font_dir = r'C:\Windows\Fonts'


def invisible_check(text):
    visible = []
    invisible = []
    for char in text:
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
    if len(visible) > 0:
        print("[+]在所选字体下的可见字符：%s" % ("".join(visible)))
    if len(invisible) > 0:
        print("[!]在所选字体下的不可见字符：%s" % (",".join(invisible)))

print("创建字体库索引...")
filelist = [os.path.join(font_dir, x) for x in os.listdir(font_dir)]
fontDb = font_dict(filelist)  # 创建字体库索引
while True:
    text = input(">>> 输入要测试的字符串:")
    invisible_check(text)
