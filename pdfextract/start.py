"""
PDF Extractor And Merger (In The Very Meantime!)

Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>

GPL
"""


import sys
sys.EXIT_SUCCESS = 0
sys.EXIT_FAILURE = 1
import logging

import PyPDF2

from .cli import parse_args
from .rangeparser import make_ranges


def main():
    """
    Start hacking.
    """
    args = parse_args()
    logging.basicConfig(
        format='%(levelname)-11s: %(message)s',
        level={
            0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG
        }[args.verbose % 3]
    )
    writer = PyPDF2.PdfFileWriter()
    for i in args.pdf_colon_ops:
        pdf_ops = i.split(':')
        file_name = pdf_ops[0]
        try:
            reader = PyPDF2.PdfFileReader(file_name)
        except Exception:
            logging.exception('Can not read: %s', file_name)
            return sys.EXIT_FAILURE

        ranges = '' if len(pdf_ops) == 1 else pdf_ops[1]
        if ranges == '':
            ranges = '1-' + str(reader.numPages)

        for i in make_ranges(ranges, reader.numPages):
            logging.info('Adding page %s of %s', i, file_name)
            if not args.test:
                try:
                    writer.addPage(reader.getPage(i - 1))
                except Exception:
                    logging.exception('Can not add page %s', i)

    sys.setrecursionlimit(args.limit * sys.getrecursionlimit())

    page_count = writer.getNumPages()
    if page_count:
        try:
            with open(args.output, 'wb') as output:
                writer.write(output)
        except Exception:
            logging.exception('Can not write: %s', args.output)
            return sys.EXIT_FAILURE
        logging.info('Exported %s page(s)', page_count)
    elif args.test:
        logging.warning('This is only a dry run')
    else:
        logging.warning('No pages in this range: %s', ranges)

    return sys.EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main())
