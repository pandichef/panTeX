# pretty-reports
Generating pretty reports using pandas and pandoc

# Notes

*  I had to add `*.md` to `.prettierignore`.  `LaTeX` equations were getting inappropriately edited.  
*  `$$` works for indicating equations on Linux.  However, for Windows, I had to use `\begin{equation}` and `\end{equation}`.  

# Image Formats

`matplotlib` apparently supports certain image formats.  I tried each one and report the results here: 
* `eps`: very nice; text can be highlighted ✔️  
* `jpeg`: just an image; text is blurry & cannot be highlighted❌  
* `jpg`: just an image; text is blurry & cannot be highlighted❌  
* `pdf`: text can be highlighted; however, the marks look distorted when zoomed out❌  
* `pgf`: returned non-zero exit status 43❌  
* `png`: just an image; text is blurry & cannot be highlighted❌  
* `ps`: it ran, the but the chart position is botched in the pdf file❌  
* `raw`: hit an infinite loop❌  
* `rgba`: hit an infinite loop❌  
* `svg`: got an exception `could not convert image`❌  
* `svgz`: got an exception `could not convert image`❌  
* `tif`: just an image; text is blurry & cannot be highlighted❌  
* `tiff`: just an image; text is blurry & cannot be highlighted❌  

# Process Flow
* string.Template is used to render a markdown template  
* `pandas.DataFrame.to_markdown` is used to create markdown tables  
* `pandoc` is used to the convert markdown file output into a pdf file (markdown 🡲 LaTeX 🡲 pdf)  

# Requirements  
* See `requirements.txt` for the Python package requirements  
* Also requires `pandoc` and `MiKTeX` to be installed (on Windows)  

# Workflow
* Develop the document using a web page using `browser-sync start --server --files "*.html" --index "output.html"`  
* Print to `pdf` when you're ready  
