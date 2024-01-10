# -*- coding:utf-8 -*-
from fontTools.ttLib import TTFont
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.misc.transform import Offset
from fontTools.pens.areaPen import AreaPen
import os


# 从系统所有字体中寻找特定字符并绘制图形
# require freetype-py,matplotlib

def display(char, GlyphSet, Cmap, font, show):
    pen = FreeTypePen(None)
    glyph_set = GlyphSet
    glyph = glyph_set[Cmap[ord(char)]]
    try:
        glyph.draw(pen)
        width, ascender, descender = glyph.width, font['OS/2'].usWinAscent, -font['OS/2'].usWinDescent
        height = ascender - descender
        if width == 0:
            width = 500
        if height == 0:
            height = 1000
        if show:
            pen.show(width=width, height=height, transform=Offset(0, -descender), contain=True)
        pen = AreaPen()
        glyph.draw(pen)
        blackarea = abs(pen.value)
        total_area = width * height
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
    if font.getBestCmap() and ord(char) in font.getBestCmap().keys():
        return True
    else:
        return False


def char2un(char):
    return r"\u%s" % hex(ord(char))[2:].zfill(4)


def SearchandDraw(char, maxDraw=-1):
    if len(char) != 1:
        char = char[0]
    found_fonts = []
    for key in fontDb.keys():
        cmap = fontDb[key]["Cmap"]
        if cmap and ord(char) in cmap.keys():
            found_fonts.append(key)

    if len(found_fonts) > 0:
        print("在 %s 中找到了该文本: %s(%s)" % ("\r\n".join(found_fonts), char, char2un(char)))
        i = 0
        for fontfile in found_fonts:
            show = 1
            if maxDraw < i:
                show = 0
            if maxDraw == -1:
                show = 1
            display(char, fontDb[fontfile]["GlyphSet"], fontDb[fontfile]["Cmap"], fontDb[fontfile]["font"], show=show)
    else:
        print("未找到该文本的字形: %s(%s)" % (char, char2un(char)))


print("创建字体库索引...")
font_dir = r"c:\windows\fonts"
filelist = [os.path.join(font_dir, x) for x in os.listdir(font_dir)]
fontDb = font_dict(filelist)  # 创建字体库索引
SearchandDraw("ㅤ", 3)
