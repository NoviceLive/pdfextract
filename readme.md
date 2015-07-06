# pdfextract
# PDF 文档摘取合并工具


## Features
## 特点

- Multiple page range support

- 支持同时摘取多个范围

- Multiple source PDFs support

- 支持同时摘取多个文件


## Dependencies
## 依赖

- [PyPDF2](https://github.com/mstamy2/PyPDF2), which can be installed via pip

- [PyPDF2](https://github.com/mstamy2/PyPDF2)，可以用 pip 安装

- [Python](https://www.python.org/)

- [Python](https://www.python.org/)，支持 Py2 和 Py3


## Usage
## 用法

See `./pdfextract.py --help`.

参见 `./pdfextract.py --help`。


## Examples
## 演示用例

1. Extracting pages from the 5th to the last
(Suppose it is no less than 5 pages)
> `pdfextract test.pdf:5-`

2. Extracting from the first page to the 5th
(Suppose it is no less than 5 pages)
> `pdfextract test.pdf:-5`

3. Removing the 6th page, naming the new pdf as no-6.pdf
(Suppose it has more than 6 pages)
> `pdfextract test.pdf:-5+7- -o no-6.pdf`

4. Tripling the source pdf
(With the same pages repeated two more times)
> `pdfextract test.pdf:++`

5. Extracting the 1st, 3rd, 5th, 7th and 9th page
(Suppose it is no less than 9 pages)
> `pdfextract test.pdf:1+3+5+7+9`


## TODO
## 改进

- Deal with encrypted PDF documents

- 添加对加密 PDF 文档的支持

- Improve the syntax since the current one seems strange.

- 改进页面范围的表示格式


## License
## 授权

GPL
