# -*- coding: utf-8 -*-


from setuptools import setup


setup(
    name = 'pdfextract',
    version = '0.1.2',

    install_requires = ['PyPDF2'],

    author = 'Gu Zhengxiong',
    author_email = 'gzxdgg@qq.com',

    description = 'PDF Extractor And Merger',
    license = 'GPLv3+',
    keywords = 'pdf extractor, pdf merger',
    url = 'https://github.com/NoviceLive/pdfextract',

    entry_points = {
        'console_scripts' : ['pdfextract=pdfextract:start_main']
        }
)
