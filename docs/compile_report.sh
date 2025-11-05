#!/bin/bash
pdflatex Dataset_report.tex
biber Dataset_report
pdflatex Dataset_report.tex
pdflatex Dataset_report.tex
