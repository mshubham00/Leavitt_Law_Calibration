#!/bin/bash
compile_latex() {
    pdflatex main.tex
    bibtex main
    pdflatex main.tex
    pdflatex main.tex
    }
    
compile_latex

#biber main
