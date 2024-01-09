from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.freetypePen import FreeTypePen
from fontTools.misc.transform import Offset
from fontTools.pens.areaPen import AreaPen
import os


# 通过字符图形的笔画比例来判断字符是否可视化
# require freetype-py,matplotlib

def display(char, font_path):
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
    try:
        glyph.draw(pen)
        blackarea = abs(pen.value)
        total_area = glyph.width * (ascender + descender)
        if total_area == 0:
            rat = 0
        else:
            rat = blackarea / total_area
    except:
        rat = -1
    return rat


def findChar(char, font_path, fontnum=-1):
    font = TTFont(font_path, fontNumber=fontnum)
    GlyphSet = font.getGlyphSet()
    index = ord(char)
    if font.getBestCmap() and index in font.getBestCmap().keys() and font.getBestCmap()[index] in list(GlyphSet.keys()):
        return True
    else:
        return False


# 指定字体文件路径
fonts = r'C:\Windows\Fonts'


def invisible_check(text):
    visible = []
    invisible = []
    for char in text:
        found_fonts = []
        for file in os.listdir(fonts):
            file = os.path.join(fonts, file)
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
                rat = display(char, fontfile)
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


while True:
    text = input(">>> 输入要测试的字符串:")
    invisible_check(text)
