# Author: Helga Nyrud
help:
	@echo "Available targets:"
	@echo "pdf"
	@echo "txt - plaintext (created from pdf)"
	@echo "tex - mostly for debugging"

pdf: tex
	@echo
	@echo "Creating pdf file from latex source"
	@echo "-----------------------------------"
	/snacks/bin/python3.3 ./pyscript/plotcourses.py -o plots/ -t .. -d . -r report.tex -m
	pdflatex report.tex

txt: pdf
	@echo
	@echo "Creating txt file from pdf "
	@echo "---------------------------"
	ps2ascii report.pdf report.txt

#Sed replaces wonky "å" chars with good one
tex:
	@echo
	@echo "Creating latex file from course summaries"
	@echo "-----------------------------------------"
	sed -i.bak 's/å/å/Ig' INF*.txt
	/snacks/bin/python3 ./pyscript/compile-summaries.py
