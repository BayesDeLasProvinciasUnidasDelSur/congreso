all: main-es.pdf main-en.pdf

main-es.pdf:
	sed -i 's/\\entrue/\\estrue/g' cv.tex
	pdflatex main.tex
	mv main.pdf main-es.pdf

main-es.pdf:
	sed -i 's/\\estrue/\\entrue/g' cv.tex
	pdflatex main.tex
	mv main.pdf main-en.pdf
