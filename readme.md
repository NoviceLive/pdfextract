# pdfextract

## Page Extractor And Merger For PDF Documents


## Dependencies

- [PyPDF2](https://github.com/mstamy2/PyPDF2), which can be installed via pip

- [Python](https://www.python.org/)


## Usage

See `./pdfextract.py --help`.


## Examples

1. Extracting pages from the 5th to the last
`pdfextract test.pdf:5-`
Suppose it is no less than 5 pages.

2. Extracting from the first page to the 5th
`pdfextract test.pdf:-5`
Suppose it is no less than 5 pages.

3. Removing the 6th page, naming the new pdf as no-6.pdf
`pdfextract test.pdf:-5+7- -o no-6.pdf`
Suppose it has more than 6 pages.

4. Tripling the source pdf
`pdfextract test.pdf:++`
With the same pages repeated two more times.

5. Extracting the 1st, 3rd, 5th, 7th and 9th page,
`pdfextract test.pdf:1+3+5+7+9`
Suppose it is no less than 9 pages.


## TODO

- Improve the syntax since the current one seems strange.


## License

GPL
