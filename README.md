# non-font-char_detector
从字符串中检测无字形的字符，即“打印出来以后是空白或是࿰这样的文本”

这类文本主要是因为当前应用使用的字体文件中，找不到这个字符编码对应的字形，导致无法打印出来形状。

脚本 font_detect_from_fonts 从系统常用的字体文件中提取未设置字形的编码。

脚本 font_detect_from_black 从系统常用的字体文件中绘制要测试的字符，通过计算图形中笔画痕迹的面积占比来找到未设置字形的编码

脚本 font_detect_from_black_allFonts 从系统所有的字体文件中绘制要测试的字符，通过计算图形中笔画痕迹的面积占比来找到未设置字形的编码

一些样本：

英语：Hello, World

德语：Hallo, Welt

俄语：Привет, мир

法语：Bonjour, le monde

菲律宾语：Hello, Mundo

韩语：안녕하세요, 세계

波斯语：سلام، دنیا

日语：こんにちは、世界

捷克语：Ahoj, světe

荷兰语：Hallo, wereld

西班牙语：Hola, mundo

意大利语：Ciao, mondo

匈牙利语：Szia, világ

希腊语：Γεια σου, κόσμ

日语：こんにちは、世界

泰语：สวัสดีชาวโลก

俄语：Привет, мир