# pdfextract

### page extractor and merger for pdf documents

## 0.1.1 -- feb 7, 2015

1. added support for multiple source documents.

now you can merge the extracted pages in the very same command, no matter where these pages are extracted from.

## 0.1.0 -- feb 6, 2015

1. rewritten from scratch, using PyPDF2, pure python.

you can extract, remove, duplicate or rearrange pages as you like.

## 0.0.5 -- feb 3, 2015

7. added support for multiple range, but changed commandline options a lot.
   no more direct option for removing pages, but this is likely to be added in later codes, in the form of syntactic sugar for extracting.
   \`-f', \`-l' and \`-r' was removed, while \`-p' took their place.

## 0.0.4 -- feb 2, 2015

6. \`eval' is evil. no \`eval' is also nice.

## 0.0.3 -- jan 29, 2015

5. let's check the sanity of that eval's argument. :)
   and also restrict the execution environment of that eval to one that only contains the \`subprocess' module,
   but it seems to be of trivial use as \`subprocess' can do a lot of evil only by itself, :(
   and the code below does not work as i expected! the environment was not restricted at all! :(
```python
   restrict_env = {'subprocess':__import__('subprocess')}
   eval('print(globals())', restrict_env)
```
   the reason is in the docs,
   \`if the globals dictionary is present and lacks ‘\_\_builtins__’, the current globals are copied into globals before expression is parsed'.
   so, am i going to write a python sandbox?
   no! at least not now! stop here! escaping is enough. let's assume it is enough. :)

## 0.0.2 -- jan 28, 2015

2. introduced \`eval' to achieve simultaneously uniting separated single pages. but! see 3.
   newly wrapped \`pdfinfo', thus there is now no need to specify the page count at commandline.

3. that eval! command injection! \`base_name' is completely under malicious attackers' control.
   invoke this script with a valid pdf document whose filename was offensively crafted.

   e.g. `test'])==__import__('os').system('rm -rf '+chr(47))#.pdf`
   the above example will \`rm -rf /'. how about \`rm -rf --no-preserve-root /'? :)
```
   $ pdfextract -l 2 test\'\]\)\=\=__import__\(\'os\'\).system\(\'rm\ -rf\ \'+chr\(47\)\)#.pdf 
   rm: it is dangerous to operate recursively on ‘/’
   rm: use --no-preserve-root to override this failsafe
```
4. \`eval' is fatally dangerous!
   all user input are also fatally detrimental!
   more priviledged, more fatally lethal!

## 0.0.1 -- jan 10, 2015

1. the initial workable version, invoking \`pdfseparate' and \`pdfunite' for every single page.
