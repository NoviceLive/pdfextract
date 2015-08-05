"""
PDF Extractor And Merger (In The Very Meantime!)

Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>

GPL
"""


import sys
sys.EXIT_SUCCESS = 0
sys.EXIT_FAILURE = 1
import argparse
import logging

import PyPDF2

from rangeparser import *


def main(args):
    writer = PyPDF2.PdfFileWriter()
    for i in args.pdf_colon_ops:
        pdf_ops = i.split(':')
        file_name = pdf_ops[0]
        try:
            reader = PyPDF2.PdfFileReader(file_name)
        except:
            logging.exception('Can not read: {}'.format(file_name))
            return sys.EXIT_FAILURE

        ranges = '' if len(pdf_ops) == 1 else pdf_ops[1]
        if ranges == '':
            ranges = '1-' + str(reader.numPages)

        for i in make_ranges(ranges, reader.numPages):
            logging.info(
                'Adding page {} of {}'.format(i, file_name)
            )
            if not args.test:
                try:
                    writer.addPage(reader.getPage(i - 1))
                except:
                    logging.exception('Can not add page {}'.format(i))

    sys.setrecursionlimit(args.limit * sys.getrecursionlimit())

    page_count = writer.getNumPages()
    if page_count:
        try:
            with open(args.output, 'wb') as output:
                writer.write(output)
        except:
            logging.exception('Can not write: {}'.format(args.output))
            return sys.EXIT_FAILURE
        logging.info('Exported {} page(s)'.format(page_count))
    elif args.test:
        logging.warning('This is only a dry run')
    else:
        logging.warning('No pages in this range: {}'.format(ranges))

    return sys.EXIT_SUCCESS


def parse_args():
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        'pdf_colon_ops',
        metavar='PDF:ranges',
        nargs='+',
        help="the source PDF and ranges"
    )
    parser.add_argument(
        '-o',
        '--output',
        default='output.pdf',
        help="use the provided file name instead of the default"
    )
    parser.add_argument(
        '-l',
        '--limit',
        default=3,
        type=int,
        help="increase recursion limit the provided times"
    )
    parser.add_argument(
        '-t',
        '--test',
        action='store_true',
        help='dry run and do not take action'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='turn on verbose mode, -vv for debugging mode'
    )

    return parser.parse_args()


description = """
DESCRIPTION
\tmanipulate pages either in the same or in different PDF documents.
\textract, remove, repeat or reorder, and if you like,
\tafter all of these manipulations, you can then merge them.
\n\tpage numbers start from 1.\n\tmultiple documents are supported.
"""


epilog = """
FULL SYNTAX
\t1. [start][-][end] specifies a range.
\n\t\tif <start> is not present or is 0 or is greater than
\t\t<end> (this <end> is that <end> which won't be greater than the page count
\t\t), then <start> will be 1; if <end> is absent or 0 or greater than
\t\t the page count, then <end> will be the page count.
\t\tyou can not leave both <start> and <end> unspecified
\t\tunless the - is also absent. if there is only a number,
\t\t then both <start> and <end> will be determined from the number.
\n\t2. + is used to combine several ranges in the same source PDF.
\n\t\tspecially, merely applying a single + means 0-0+0-0.
\t\tthus only using + will double the pdf, ++ will triple it, and so on.
\n\t3. under these two syntax, full freedom is granted.
"""


def start_main():
    args = parse_args()

    logging.basicConfig(
        format='%(levelname)-11s: %(message)s',
        level={
            0: logging.WARNING,
            1: logging.INFO,
            2: logging.DEBUG
        }[args.verbose % 3]
    )

    return main(args)


if __name__ == '__main__':
    sys.exit(start_main())
