# First we need to copy the .yml data into the content.tex frontmatter
python gen_frontmatter.py
# That will generate content.tex, which we now use to fill template.tex, producing output.tex
jtex freeform template.tex content.tex --output-tex output.tex
pdflatex --shell-escape -synctex=1 -interaction=nonstopmode output.tex
#$timestamp = Get-Date -UFormat "%Y-%m-%d"
timestamp=$(date +%Y-%m-%d)
fname="Lastname_CV_${timestamp}.pdf"
mkdir -p outputs
cp output.pdf "./outputs/${fname}"
