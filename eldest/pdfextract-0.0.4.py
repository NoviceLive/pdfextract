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

def separate(pdf_file, start, end, verbose=False):
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

def unite(base_name, *page_range):
    success = True
    
    start1, end1 = page_range[0:2]
    body = ['temp-' + str(i) + '-separated.pdf' for i in range(start1, end1 + 1)]
    tail = base_name + '.' + str(start1) + '-' + str(end1)
    
    if page_range[2:4]:
        start2, end2 = page_range[2:4]
        body += ['temp-' + str(i) + '-separated.pdf' for i in range(start2, end2 + 1)]
        tail += '.' + str(start2) + '-' + str(end2)

    tail += '.pdf'
    
    try:
        subprocess.check_call(['pdfunite'] + body + [tail])
    except:
        success = False
        
    [os.remove('temp-' + str(i) + '-separated.pdf') for i in range(start1, end1 + 1)]
    if page_range[2:4]:
        start2, end2 = page_range[2:4]
        [os.remove('temp-' + str(i) + '-separated.pdf') for i in range(start2, end2 + 1)]

    return success

def main():
    parser = argparse.ArgumentParser(description='extract or remove pages from pdf documents, default to extracting')
    parser.add_argument('pdf',
                        metavar='pdf_document',
                        help='the source pdf document to extract or remove from')
    parser.add_argument('-f',
                        '--from',
                        dest='start',
                        type=int,
                        metavar='start_page', 
                        help='the starting page inclusively, default to the first')
    parser.add_argument('-l',
                        '--last',
                        dest='end',
                        type=int,
                        metavar='end_page',
                        help='the ending page inclusively, default to the last')
    parser.add_argument('-o',
                        '--output',
                        dest='output',
                        metavar='filename',
                        help='output filename, default to the original name suffixed with page range')
    parser.add_argument('-r',
                        '--remove',
                        dest='remove',
                        action='store_const',
                        const=True,
                        default=False,
                        help='remove pages, instead of extracting')
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
    
    start = args.start if args.start != None else 1
    end = args.end if args.end != None else page_count
    
    if 1 <= start <= end and end - start != page_count - 1:
        base_name = args.output if args.output else os.path.splitext(os.path.basename(args.pdf))[0]

        if args.remove:
            if start == 1:
                separate(args.pdf, end + 1, page_count, args.verbose)
                unite(base_name, end + 1, page_count)
            elif end == page_count:
                separate(args.pdf, 1, start - 1, args.verbose)
                unite(base_name, 1, start - 1)
            else:
                separate(args.pdf, 1, start - 1, args.verbose)
                separate(args.pdf, end + 1, page_count, args.verbose)
                unite(base_name, 1, start -1, end + 1, page_count)
        else:
            separate(args.pdf, start, end, args.verbose)
            unite(base_name, start, end)
    else:
        print('nonsense input: page count {}, starting page {}, ending page {}'.format(page_count, start, end))

if __name__ == '__main__':
    main()
