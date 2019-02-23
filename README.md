# Convert-ebook 
[![Build Status][travis-ci]][travis-ci]
[![Build Status][appveyor]][appveyor]

>使用python3编写的电子书格式转换工具,
将未加解密的azw3格式无损转换epub,mobi
> 支持MacOS、Windows、Linux平台。


## 使用的开源工具
- [kindleunpack](https://github.com/kevinhendricks/KindleUnpack) 转换azw3为epub
- [kindlegen](http://www.amazon.com/gp/feature.html?docId=1000765211) 转换epub为mobi

## 使用方式
  
  在[release](https://github.com/Yihy/convert-ebook/releases)页面下载对应您操作系统的包
  
  ### Windows
  
  - 直接拖动文件或文件夹到convert-ebook.exe文件上即可执行
  - 命令行下使用 `./convert-ebook.exe 文件或目录`
  
  ### macOS
  
  在终端中输入
  ```bash
  chmod +x ./convert-ebook-macos
  ./convert-ebook-macos '文件或目录'
  ```
  
  ### Linux
  
  同样在终端中输入
  
   ```bash
   chmod +x ./convert-ebook-macos
    ./convert-ebook-linux '文件或目录'
   ```
  
  ### 使用源码
  ```bash
  # 第一次需要安装 threadpool
  pip install threadpool
  # 运行转换
  python ./convert-ebook.py "/doc/ebook/"
  ```
 如果不能使用`pip install threadpool`安装，请访问[threadpool主页](https://chrisarndt.de/projects/threadpool/)进行下载安装
 
请使用python3运行脚本，未做python2的支持
 
 执行脚本后，会扫描该文件或该目录下所有的azw3文件（包括子目录），并执行转换。转换后的文件会写入到azw3所在的目录。如果写入时已经存在同名文件，旧文件会被覆盖掉。
 **默认同时处理cpu核心数*2个转换任务**


## 问题
- 暂不支持epub直接转mobi，kindlegen转epub可能会导致输出的mobi文件中文乱码，暂未找到解决办法
- 暂未支持kindleunpack转换epub配置epub v2、v3、auto等参数

 
[latest-release]: https://github.com/Yihy/convert-ebook/releases/latest?svg=true
[travis-ci]: https://travis-ci.org/Yihy/convert-ebook.svg?branch=master
[appveyor]: https://ci.appveyor.com/api/projects/status/hsl74dpd01y3rsht?svg=true
