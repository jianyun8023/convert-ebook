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
  # 第一次需要安装依赖
  pip install -r requirements.txt
  # 运行转换
  python ./convert-ebook.py "/doc/ebook/"
  ``` 
请使用python3运行脚本，未做python2的支持
 
 执行脚本后，会扫描该文件或该目录下所有的azw3文件（包括子目录），并执行转换。转换后的文件会写入到azw3所在的目录。如果写入时已经存在同名文件，旧文件会被覆盖掉。
 **默认同时处理cpu核心数*2个转换任务**

## 参数
<pre>
positional arguments:
  source                specify file or dir

optional arguments:
  -h, --help            show this help message and exit
  -t THREAD_COUNT, --thread_count THREAD_COUNT
                        specify threadCount,default is cpu_count*2
  -E EPUB_VERSION, --epub_version EPUB_VERSION
                        specify EPUB version to unpack to: 2, 3 or A (for
                        automatic) or F for Force to EPUB2, default is 2
</pre>

## 问题
- 暂不支持epub直接转mobi，kindlegen转epub可能会导致输出的mobi文件中文乱码，~~暂未找到解决办法~~ 已经找到解决办法，后续增加epub->mobi
- ~~暂未支持kindleunpack转换epub配置epub v2、v3、auto等参数~~已支持

## 计划支持
- 支持的转换流程
   - azw3->mobi
   - mobi->epub
   - epub->mobi
- ~~通过参数配置输出策略~~已完成
- 通过调用calibre-cli进行书库的批量转换，增加
- calibre插件暂不考虑

[latest-release]: https://github.com/Yihy/convert-ebook/releases/latest?svg=true
[travis-ci]: https://travis-ci.org/Yihy/convert-ebook.svg?branch=master
[appveyor]: https://ci.appveyor.com/api/projects/status/hsl74dpd01y3rsht?svg=true
