# Paper Engine

**Paper Engine**（下称程序） 是一个便于用户从文献网站下载文献资源的集成工具，程序仅负责从网页中提取信息，不进行任何破解/攻击行为，如有侵权请告知。程序利用 [*Pyside6*](https://wiki.qt.io/Qt_for_Python) 进行 GUI 窗口设计，从论文查询或下载平台通过网络爬虫的方式进行论文的搜索以及下载，实现集成化的文献搜索。

## 依赖

程序使用 [*Python 3.8*](https://www.python.org/downloads/release/python-380/) 作为编程语言，依赖 [*Pyside6*](https://wiki.qt.io/Qt_for_Python) 进行 GUI 窗口设计及实现。程序所处理的文献信息通过 [*requests*](https://requests.readthedocs.io/en/latest/) 进行爬取/收集，文献所涉及的元数据通过 [*BeautifulSoup*](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 对网页进行分析得到。程序对以上依赖的版本所示如下：

```txt
requests==2.28.2
PySide6==6.5.0
bs4==0.0.1
```

在配置好 Python 后，你可以通过进入当前文件夹并运行

```bash
pip install -r requirements.txt
```

进行依赖的配置。

## 运行

使用 `python src/main.py` 运行程序，你就可以体验啦  ^ - ^ !
