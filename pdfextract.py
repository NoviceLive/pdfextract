# -*- coding: utf-8 -*-


"""
PDF Extractor And Merger

Copyright 2015 Gu Zhengxiong <rectigu@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


import sys
sys.EXIT_SUCCESS = 0
sys.EXIT_FAILURE = 1
import re
import argparse
import traceback

import PyPDF2


def main(args):
    writer = PyPDF2.PdfFileWriter()
    for i in args.pdf_colon_ops:
        pdf_ops = i.split(':')
        pdf = pdf_ops[0]
        ranges = '' if len(pdf_ops) == 1 else pdf_ops[1]

        try:
            reader = PyPDF2.PdfFileReader(pdf)
        except:
            print('could not read: {}'.format(pdf))
            if args.verbose:
                traceback.print_exc()
            return sys.EXIT_FAILURE

        if ranges == '':
            ranges = '1-' + str(reader.numPages)
        page_ranges = parse_ranges(ranges)
        if page_ranges:
            try:
                for j in page_ranges:
                    for i in make_range(j, reader.numPages):
                        writer.addPage(reader.getPage(i))
                        if args.verbose:
                            print('adding page {} from {}'.format(i + 1, pdf))
            except:
                print('add page error')
                if args.verbose:
                    traceback.print_exc()
        else:
            print('no valid range in the specified ranges: {}'.format(ranges))

    sys.setrecursionlimit(args.limit * sys.getrecursionlimit())
    page_count = writer.getNumPages()
    if page_count:
        try:
            with open(args.output, 'wb') as output:
                writer.write(output)
        except:
            print('could not write: {}'.format(args.output))
            if args.verbose:
                traceback.print_exc()
            return sys.EXIT_FAILURE
        print('exported {} page(s) successfully'.format(page_count))
    else:
        print('no valid page in the specified operations: {}'.format(ranges))

    return sys.EXIT_SUCCESS


def make_range(page_range, page_count):
    start, end = page_range
    end = end if end and end <= page_count else page_count
    start = start - 1 if start and start <= end else 0

    return range(start, end)


def parse_ranges(ranges_string):
    return [
        parse_range(i)
            for i in ranges_string.split('+') if check_range(i)
    ]


def parse_range(range_string):
    if range_string == '':
        return 1, 0

    if range_string.endswith('-'):
        range_string += '0'
    if range_string.startswith('-'):
        range_string = '1' + range_string

    single_range = range_string.split('-')
    start = int(single_range[0])
    end = int(single_range[1]) if len(single_range) == 2 else start

    return start, end


def check_range(range_string):
    if range_string == '':
        return True
    if re.sub(r'\d+\-\d+|\d+\-|\-\d+|\d+', '', range_string, 1) == '':
        return True

    return False


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
        '-v',
        '--verbose',
        action='store_true',
        help="turn on verbose mode"
    )

    return parser.parse_args()


description = """
DESCRIPTION
\tmanipulate pages either in the same PDF or in different PDF documents.
\textract, remove, repeat or reorder, and if you like,
\tafter all of these manipulations, you can then merge them.
\n\tpage numbers start from 1.\n\tmultiple source documents is supported.
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
    return main(args)


if __name__ == '__main__':
    sys.exit(start_main())
