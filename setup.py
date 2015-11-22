"""
PDF Extractor And Merger (In The Very Meantime!)

Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>

GPL
"""


from setuptools import setup


setup(
    name='pdfextract',
    version='0.1.2',
    packages=['pdfextract'],
    entry_points={
        'console_scripts' : ['pdfextract=pdfextract.start:main']
    },
    install_requires=['PyPDF2'],

    author='Gu Zhengxiong',
    author_email='gzxdgg@qq.com',

    description='PDF extractor, and in the very meantime, ' \
    'merger, based on PyPDF2',
    license='GPL',
    keywords='PDF Extract, PDF Split, PDF Merge',
    url='https://github.com/NoviceLive/pdfextract',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
