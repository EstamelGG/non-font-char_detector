from fontTools.ttLib import TTFont


def find_missing_glyphs(font_path,fontnum=-1):
    # 加载字体文件
    font = TTFont(font_path,fontNumber=fontnum)

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
            invisible.append(str(ord(char)))
        else:
            visible.append(char)
    return invisible, visible


# 指定字体文件路径
font_path = r'C:\Windows\Fonts\segoeui.ttf'  # 英文字体
en_font_missing = find_missing_glyphs(font_path)

font_path = r'C:\Windows\Fonts\msyh.ttc'  # 微软雅黑
cn_font_missing = find_missing_glyphs(font_path, 0)  # ttc文件需要参数 0

missing = list(set(en_font_missing) & set(cn_font_missing))   # 取交集

# 打印缺失的Unicode字符编码
print(f"Missing glyphs count: {len(missing)}")
while True:
    text = input(">>> input: ")
    invisible, visible = check_string(str(text), missing)
    if len(invisible) > 0:
        print("<<< [!]存在不可见字符: %s" % (",".join(invisible)))
        print("<<< [!]可见部分: %s" % ("".join(visible)))
    else:
        print("<<< [+]均可见: %s" % ("".join(visible)))
