"""
PDF Extractor And Merger (In The Very Meantime!)

Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>

GPL
"""


import argparse


def parse_args():
    """
    Parse the arguments.
    """
    parser = argparse.ArgumentParser(
        description=DESCRIPTION, epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'pdf_colon_ops', metavar='PDF:ranges', nargs='+',
        help="the source PDF and ranges"
    )
    parser.add_argument(
        '-o', '--output', default='output.pdf',
        help="use the provided file name instead of the default"
    )
    parser.add_argument(
        '-l', '--limit', default=3, type=int,
        help="increase recursion limit the provided times"
    )
    parser.add_argument(
        '-t', '--test', action='store_true',
        help='dry run and do not take action'
    )
    parser.add_argument(
        '-v', '--verbose', action='count', default=0,
        help='turn on verbose mode, -vv for debugging mode'
    )
    return parser.parse_args()


DESCRIPTION = """
DESCRIPTION
\tmanipulate pages either in the same or in different PDF documents.
\textract, remove, repeat or reorder, and if you like,
\tafter all of these manipulations, you can then merge them.
\n\tpage numbers start from 1.\n\tmultiple documents are supported.
"""


EPILOG = """
FULL SYNTAX
\t1. [start][-][end] specifies a range.
\n\t\tif <start> is not present or is 0 or is greater than
\t\t<end> (this <end> is that <end> which won't be greater than
\t\t the page count),
\t\tthen <start> will be 1; if <end> is absent or 0 or greater than
\t\t the page count, then <end> will be the page count.
\t\tyou can not leave both <start> and <end> unspecified
\t\tunless the - is also absent. if there is only a number,
\t\t then both <start> and <end> will be determined from the number.
\n\t2. + is used to combine several ranges in the same source PDF.
\n\t\tspecially, merely applying a single + means 0-0+0-0.
\t\tthus only using + will double the pdf, ++ will triple it,
\t\tand so on.
\n\t3. under these two syntax, full freedom is granted.
"""
