#!/usr/bin/env python3


"""
PDF Extractor And Merger

Copyright (C) 2015 谷征雄 (rectigu@gmail.com, http://novicelive.org/)

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


import re
import argparse
import sys
import traceback

import PyPDF2


def main(args):
    if not args.output:
        args.output = 'output.pdf'

    writer = PyPDF2.PdfFileWriter()

    for i in args.pdf_colon_ops:
        pdf_ops_list = i.split(':')
        if len(pdf_ops_list) == 2:
            pdf, pages = pdf_ops_list
        else:
            pdf = pdf_ops_list[0]
            pages = ''
        try:
            reader = PyPDF2.PdfFileReader(
                pdf,
                warndest=None if args.verbose else sys.stdin
            )
        except:
            print('could not read: {}'.format(pdf))
            if args.verbose:
                traceback.print_exc()
            exit()

        if pages == '':
            pages = '1-' + str(reader.numPages)

        page_ranges = parse_page_ranges(pages)
        if page_ranges:
            try:
                [
                    [
                        writer.addPage(reader.getPage(i))
                        ==
                        (
                            print('adding page {} from {}'.format(i + 1, pdf))
                            if args.verbose else None
                        )

                        for i in make_single_range(j, reader.numPages)
                    ]
                    for j in page_ranges
                ]
            except:
                print('add page error')
                if args.verbose:
                    traceback.print_exc()
        else:
            print('no valid range in the specified ranges: {}'.format(pages))

    total_page_count = writer.getNumPages()

    # let's take some risk
    sys.setrecursionlimit(4 * sys.getrecursionlimit())

    if total_page_count:
        try:
            with open(args.output, 'wb') as output:
                writer.write(output)
        except:
            print('could not write: {}'.format(args.output))
            if args.verbose:
                traceback.print_exc()
            exit()

        print('exported {} page(s) successfully'.format(total_page_count))
    else:
        print('no valid page in the specified operations: {}'.format(pages))


def parse_page_ranges(raw_range_string):
    """
    parse the commandline string,
    which specifies how to behave, into a usable form

    + param str raw_range_string:
        the raw string containing information about page rangs

    + return: all valid page ranges, each of them are in the form (start, end)
    + rtype: list
    """
    return [parse_single_range(i)
            for i in raw_range_string.split('+') if check_single_range(i)]


def make_single_range(page_range, page_count):
    """
    correct a single range, i.e.,
    convert 1-indexed-from to 0-indexed-from
    and replace illegal vaule to conventionally defined value

    + param tuple page_range:
        in the form (start, end),
        both <start> and <end> are 1-indexed-from.

    + param int page_count:
        the page count of the source pdf,
        used to correct out-of-bound invalid upper range

    + return: a range instance,
        producing values exactly the same in the input range,
        except here are 0-indexed-from

    + rtype: range
    """
    # here are indexed from 1
    start, end = page_range
    # <end> do not need to subtract 1
    # because range() itself will not produce to its upper bound
    end = end if end and end <= page_count else page_count
    #  # <start> has to be decremented by 1
    start = start - 1 if start and start <= end else 0
    # directly return a range instance rather than a tuple
    return range(start, end)


def parse_single_range(single_range_string):
    """
    parse separated single range strings into a tuple.
    in the form of (start, end)

    + param str single_range_string:
        a string of the form [start][-][end], which specifies a range

    + return: (start, end)
    + rtype: tuple
    """
    if not single_range_string:
        return 1, 0

    if single_range_string.endswith('-'):
        single_range_string += str(0)
    if single_range_string.startswith('-'):
        single_range_string = str(1) + single_range_string

    single_range = single_range_string.split('-')
    start = int(single_range[0])
    end = int(single_range[1]) if len(single_range) == 2 else start
    return start, end


def check_single_range(single_range_string):
    """
    check the validity of a single range string before it can be parsed

    + param str single_range_string:
        a string of the form [start][-][end], which specifies a range

    + return true if valid else false
    + rtype: boolean
    """
    if single_range_string:
        # re.fullmatch became available since python 3.4.
        # compatibility troubles.
        # if re.fullmatch(r'\d+\-|\-\d+|\d+\-\d+', single_range_string):
        # move \d+\-\d to the first or this will not be right
        if not re.sub(r'\d+\-\d+|\d+\-|\-\d+|\d+', '', single_range_string, 1):
            return True
        else:
            print('syntax error: {}'.format(single_range_string))
            return False
    return True


def parse_args():
    parser = argparse.ArgumentParser(
        description="""DESCRIPTION
\tmanipulate pages either in the same pdf or in different pdf documents
\textract, remove, repeat or reorder, and if you like,
\tafter all of these manipulations, you can then merge them
\tpage numbers start from 1\n\n\tsupport multiple source documents""",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('pdf_colon_ops', metavar='pdf_document:page_ranges',
                        nargs='+',
                        help="""the source document to operate on
and the page ranges (full syntaxes see below). only specifying the pdf file
means the whole document is targeted, i.e. 0-0 (see below :))""")

    parser.add_argument('-o', '--output', metavar='pdf_output', dest='output',
                        help="""do not use the default output name
(which is output.pdf).
export the resulting document with the specified file name""")

    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        help="""display more error and warning information,
as well as what is going on""")

    return parser.parse_args()


epilog = """
FULL PAGE RANGE SYNTAX
\t1. [start][-][end] specifies a single page range.

\t\tif <start> is not present or is 0 or is greater than
\t\t<end> (this <end> is that <end> which won't be greater than the page count
\t\t), then <start> will be 1; if <end> is absent or 0 or greater than
\t\t the page count, then <end> will be the page count.
\t\tyou can not leave both <start> and <end> unspecified
\t\tunless the - is also absent. if there is only a number,
\t\t then both <start> and <end> will be determined from the number.

\t2. + is used to combine several single page ranges.

\t\tspecially, merely applying a single + means 0-0+0-0.
\t\tthus only using + will double the pdf, ++ will triple it, and so on.

\t3. under these two syntaxes, freedom is granted.
"""


if __name__ == '__main__':
    args = parse_args()
    try:
        main(args)
    except KeyboardInterrupt:
        print('user cancelled')
