#!/usr/bin/env python3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#     pdfextract.py by Novice Live, http://novicelive.org/ :)
#
#     extract or remove pages from pdf documents, default to extracting.
#     merely a wrapper of `pdfseparate', `pdfunite' and `pdfinfo', which are all from the package `poppler-utils'.
#
#     1. the initial workable version, invoking `pdfseparate' and `pdfunite' for every single page.
#
#     jan 10 2015
#
#     2. introduced `eval' to achieve simultaneously uniting separated single pages. but! see 3.
#        newly wrapped `pdfinfo', thus there is now no need to specify the page count at commandline.
#
#     3. that eval! command injection! `base_name' is completely under malicious attackers' control.
#        invoke this script with a valid pdf document whose filename was offensively crafted.
#
#        e.g. test'])==__import__('os').system('rm -rf '+chr(47))#.pdf
#        the above example will `rm -rf /'. how about `rm -rf --no-preserve-root /'? :)
#
#        $ pdfextract -l 2 test\'\]\)\=\=__import__\(\'os\'\).system\(\'rm\ -rf\ \'+chr\(47\)\)#.pdf 
#        rm: it is dangerous to operate recursively on ‘/’
#        rm: use --no-preserve-root to override this failsafe
#
#     4. `eval' is fatally dangerous!
#        all user input are also fatally detrimental!
#        more priviledged, more fatally lethal!
#
#     jan 28, 2015
#
#     5. let's check the sanity of that eval's argument. :)
#        and also restrict the execution environment of that eval to one that only contains the `subprocess' module,
#        but it seems to be of trivial use as `subprocess' can do a lot of evil only by itself, :(
#        and the code below does not work as i expected! the environment was not restricted at all! :(
#
#        restrict_env = {'subprocess':__import__('subprocess')}
#        eval('print(globals())', restrict_env)
#
#        the reason is in the docs,
#        `if the globals dictionary is present and lacks ‘__builtins__’, the current globals are copied into globals before expression is parsed'.
#        so, am i going to write a python sandbox?
#        no! at least not now! stop here! escaping is enough. let's assume it is enough. :)
#
#     jan 29, 2015
#
#     6. `eval' is evil. no `eval' is also nice.
#
#     feb 2, 2015
#
#     7. added support for multiple range, but changed commandline options a lot.
#        no more direct option for removing pages, but this is likely to be added in later codes, in the form of syntactic sugar for extracting.
#        `-f', `-l' and `-r' was removed, while `-p' took their place.
#
#     feb 3, 2015
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#     Copyright (C) 2015  Gu Zhengxiong
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import sys
import subprocess
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='extract or remove pages from pdf documents, default to extracting; extracting only needed pages is equivalent to removing unneeded ones :)')
    parser.add_argument('pdf',
                        metavar='pdf_document',
                        help='the source pdf document to extract from')
    parser.add_argument('-p',
                        '--pages',
                        dest='pages',
                        metavar='page_ranges',
                        required=True,
                        help='page ranges to extract, e.g. 1-10+12-30; 56-100+110-, padding \'-\' means processing to the last page')
    parser.add_argument('-o',
                        '--output',
                        dest='output',
                        metavar='filename',
                        help='output filename, default to the original name suffixed with the page range')
    parser.add_argument('-v',
                        '--verbose',
                        dest='verbose',
                        action='store_const',
                        const=True,
                        default=False,
                        help='verbosely output with error information')
   
    args = parser.parse_args()
    
    page_count = count_page(args.pdf)
    if not page_count:
        print('error processing {}: could not get page count of the specified document'.format(args.pdf))
        exit()
        
    if args.pages.endswith('-'):
        args.pages += str(page_count)
        
    range_list = parse_page_range(args.pages)
    if range_list == False:
        print('syntax error: {}'.format(args.pages))
        exit()

    base_name = args.output if args.output else os.path.splitext(os.path.basename(args.pdf))[0]

    [separate(args.pdf, i, args.verbose) for i in range_list]
    
    unite_args = []
    for i in range_list:
        unite_args += make_unite_args(i)
    unite_args.append(base_name + ' (' + args.pages + ').pdf')
    
    invoke_pdfunite(unite_args)

    [clean_single_page(i) for i in range_list]

def count_page(pdf_file):
    try:
        pdfinfo_ret = subprocess.check_output(
            ['pdfinfo', pdf_file],
            stderr=subprocess.DEVNULL).decode('utf-8')
    except:
        return False

    for i in pdfinfo_ret.split('\n'):
        if 'Pages:' in i:
            return int(i.lstrip('Pages:'))
    return False

def separate(pdf_file, page_range, verbose):
    start, end = page_range
    try:
        subprocess.check_call(
            ['pdfseparate',
             '-f',
             str(start),
             '-l',
             str(end),
             pdf_file,
             'temp-%d-separated.pdf'],
            stderr=subprocess.DEVNULL if not verbose else None)
    except:
        return False
    return True

def invoke_pdfunite(args):
    try:
        subprocess.check_call(['pdfunite'] + args)
    except:
        return False
    return True

def parse_page_range(page_ranges):
    try:
        return [(lambda x:[int(i) for i in x.split('-')])(j) for j in page_ranges.split('+')]
    except:
        return False

def make_page_string(page):
    return 'temp-' + str(page) + '-separated.pdf'

def make_unite_args(page_range):
    start, end = page_range
    return [make_page_string(i) for i in range(start, end + 1)]

def clean_single_page(page_range):
    start, end = page_range
    [os.remove(make_page_string(i)) for i in range(start, end + 1)]

if __name__ == '__main__':
    main()
