# Convert-ebook

>使用python3编写的电子书格式转换工具,
将未加解密的azw3格式无损转换epub,mobi
> 支持MacOS、Windows、Linux平台。

## 使用的开源工具
- kindleunpack 转换azw3为epub
- kindlegen 转换epub为mobi

## 使用方式

请使用python3运行脚本，未做python2的支持
 `python ./convert-ebook.py [文件存放目录]`
 
执行脚本后，会扫描该目录下所有的azw3文件（包括子目录），并执行转换。转换后的文件会写入到azw3所在的目录。如果写入时已经存在同名文件，源文件会被覆盖掉


## 问题
- 暂不支持epub直接转mobi，kindlegen转epub可能会导致输出的mobi文件中文乱码，暂未找到解决办法
- 暂未支持kindleunpack转换epub配置epub v2、v3、auto等参数

 