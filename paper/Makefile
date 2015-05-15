all: 2014-streaming.pdf

2014-streaming.pdf: 2014-streaming.tex 2014-streaming.bib
	pdflatex 2014-streaming.tex
	bibtex 2014-streaming
	pdflatex 2014-streaming.tex
	pdflatex 2014-streaming.tex
	pdflatex 2014-streaming.tex

clean:
	rm 2014-streaming.pdf *.aux
