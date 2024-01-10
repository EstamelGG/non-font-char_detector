from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.misc.transform import Offset
from fontTools.pens.areaPen import AreaPen
import os

# 从系统所有字体中寻找特定字符并绘制图形
# require freetype-py,matplotlib

def display(char, font_path, show):
    if str(font_path).endswith(".ttf"):
        fontnum = -1
    elif str(font_path).endswith(".ttc"):
        fontnum = 0
    else:
        return 0
    font = TTFont(font_path, fontNumber=fontnum)
    pen = FreeTypePen(None)
    glyph_set = font.getGlyphSet()
    glyph = glyph_set[font.getBestCmap()[ord(char)]]
    try:
        glyph.draw(pen)
        width, ascender, descender = glyph.width, font['OS/2'].usWinAscent, -font['OS/2'].usWinDescent
        height = ascender - descender
        if show:
            pen.show(width=width, height=height, transform=Offset(0, -descender))
        pen = AreaPen()
        glyph.draw(pen)
        blackarea = abs(pen.value)
        total_area = glyph.width * (ascender + descender)
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


def char2un(char):
    return r"\u%s" % hex(ord(char))[2:].zfill(4)

def SearchandDraw(char):
    if len(char) != 1:
        char = char[0]
    font_dir = r"c:\windows\fonts"
    found_fonts = []
    for file in os.listdir(font_dir):
        file = os.path.join(font_dir, file)
        if str(file).endswith(".ttf"):
            fontnum = -1
        elif str(file).endswith(".ttc"):
            fontnum = 0
        else:
            continue
        if findChar(char, file, fontnum):
            found_fonts.append(file)

    if len(found_fonts) > 0:
        print("在 %s 中找到了该文本: %s(%s)" % ("\r\n".join(found_fonts), char, char2un(char)))
        for fontfile in found_fonts:
            rat = display(char, fontfile, show=1)
    else:
        print("未找到该文本的字形: %s(%s)" % (char, char2un(char)))

SearchandDraw("ㅤ")


