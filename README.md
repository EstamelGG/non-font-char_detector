# non-font-char_detector
从字符串中检测无字形的字符，即“打印出来以后是空白或是࿰这样的文本”

这类文本主要是因为当前应用使用的字体文件中，找不到这个字符编码对应的字形，导致无法打印出来形状。

该脚本从系统默认的微软雅黑和Segoe UI两个字体文件中提取未设置字形的编码。
