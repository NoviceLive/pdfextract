# pdfextract

## Features

- Multiple page range support

- Multiple source PDFs support


## Installation

```
sudo pip install pdfextract
```


## Usage

See `./pdfextract.py --help`.


## Examples

1. Extracting pages from the 5th to the last
(Suppose it is no less than 5 pages)
> `pdfextract test.pdf:5-`

2. Extracting from the first page to the 5th
(Suppose it is no less than 5 pages)
> `pdfextract test.pdf:-5`

3. Removing the 6th page, naming the new pdf as no-6.pdf
(Suppose it has more than 6 pages)
> `pdfextract test.pdf:-5+7- -o no-6.pdf`

4. Tripling the source pdf
(With the same pages repeated two more times)
> `pdfextract test.pdf:++`

5. Extracting the 1st, 3rd, 5th, 7th and 9th page
(Suppose it is no less than 9 pages)
> `pdfextract test.pdf:1+3+5+7+9`


## TODO

- Deal with encrypted PDF documents

- Improve the syntax since the current one seems strange.


## License

GPL

## Related Projects

- [pdfcat](https://github.com/mstamy2/PyPDF2/blob/master/Scripts/pdfcat)

  It comes with PyPDF2, and uses a slice-like syntax, which is more flexible.
