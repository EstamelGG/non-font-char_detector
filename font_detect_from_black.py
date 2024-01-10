# -*- coding:utf-8 -*-
from fontTools.ttLib import TTFont
from fontTools.pens.areaPen import AreaPen


# 通过字符图形的笔画比例来判断字符是否可视化
# require freetype-py,matplotlib

def display(char, font_path, show):
    if str(font_path).endswith(".ttf"):
        fontnum = -1
    elif str(font_path).endswith(".ttc"):
        fontnum = 0
    else:
        return 0
    font = TTFont(font_path, fontNumber=fontnum)
    pen = AreaPen()
    glyph_set = font.getGlyphSet()
    glyph = glyph_set[font.getBestCmap()[ord(char)]]
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


# 指定字体文件路径
fonts = [
    r'C:\Windows\Fonts\segoeui.ttf',  # windows系统默认
    r'C:\Windows\Fonts\arial.ttf',  # arial,常用字体
    r'C:\Windows\Fonts\msyh.ttc',  # 微软雅黑
    r'C:\Windows\Fonts\msjh.ttc',  # 微软正黑
    r'C:\Windows\Fonts\malgun.ttf',  # 韩语
    r'C:\Windows\Fonts\msgothic.ttc',  # 日语
    r'C:\Windows\Fonts\LeelawUI.ttf',  # 泰语
]


def invisible_check(text):
    visible = []
    invisible = []
    for char in text:
        found_fonts = []
        for file in fonts:
            if str(file).endswith(".ttf"):
                fontnum = -1
            elif str(file).endswith(".ttc"):
                fontnum = 0
            else:
                continue
            if findChar(char, file, fontnum):
                found_fonts.append(file)

        if len(found_fonts) > 0:
            ratlist = []
            for fontfile in found_fonts:
                rat = display(char, fontfile, show=0)
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


print("检测的目标字体：")
for i in fonts:
    print(i)
while True:
    text = input(">>> 输入要测试的字符串:")
    invisible_check(text)
