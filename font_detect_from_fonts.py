# -*- coding:utf-8 -*-
from fontTools.ttLib import TTFont

#通过特定字体文件的字符映射表来判断是否字符可见，实际上是检测字符串中的unicode编码是否都分配了字符

def find_missing_glyphs(font_path, fontnum=-1):
    # 加载字体文件
    font = TTFont(font_path, fontNumber=fontnum)

    # 获取字体中所有的字符映射
    cmap = font['cmap']
    glyph_set = font.getGlyphSet()

    # 获取所有的Unicode字符映射
    unicode_cmap = next(c for c in cmap.tables if c.platformID == 3 and c.platEncID in [1, 10])
    unicode_map = unicode_cmap.cmap

    # 找到没有对应符号的Unicode字符
    missing_glyphs = []
    for codepoint in range(0x110000):  # 遍历所有可能的Unicode编码
        if codepoint not in unicode_map or unicode_map[codepoint] not in glyph_set:
            missing_glyphs.append(codepoint)

    return missing_glyphs


def check_string(string, missing_glyphs):
    visible = []
    invisible = []
    for char in string:
        if ord(char) in missing_glyphs:
            invisible.append(r"\u%s" % hex(ord(char))[2:].zfill(4))
        else:
            visible.append(char)
    return invisible, visible


def missed_fonts_extra(files):
    ttc_missed = set()
    missed = set()
    for fontfile in files:
        if str(fontfile).endswith(".ttc"):
            ttc_missed = find_missing_glyphs(fontfile, 0)  # ttc文件需要参数 0
        elif str(fontfile).endswith(".ttf"):
            ttc_missed = find_missing_glyphs(fontfile)
        if len(missed) == 0:
            missed = set(ttc_missed)
        missed = missed.intersection(ttc_missed)
    return missed


# 指定字体文件路径
fonts = [
    r'C:\Windows\Fonts\segoeui.ttf',  # windows系统默认
    r'C:\Windows\Fonts\arial.ttf',  # arial,常用字体
    r'C:\Windows\Fonts\msyh.ttc',  # 微软雅黑
    r'C:\Windows\Fonts\msjh.ttc',  # 微软正黑
    r'C:\Windows\Fonts\malgun.ttf',  # 韩语
    r'C:\Windows\Fonts\msgothic.ttc',  # 日语
]

missing = missed_fonts_extra(fonts)

# 打印缺失的Unicode字符编码
print(f"Missing glyphs count: {len(missing)}")
while True:
    text = input(">>> input: ")
    invisible, visible = check_string(str(text), missing)
    if len(invisible) > 0:
        print("<<< [!]存在未分配字符的编码: %s" % (",".join(invisible)))
        print("<<< [!]有字符部分: %s" % ("".join(visible)))
    else:
        print("<<< [+]均有字符: %s" % ("".join(visible)))
