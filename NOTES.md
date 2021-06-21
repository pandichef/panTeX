# Image Formats

`matplotlib` supports certain image formats.  I tried each one and report the results here: 
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

# Miscellaneous

*  I had to add `*.md` to `.prettierignore`.  `LaTeX` equations were getting inappropriately edited in vscode.  
*  `$$` works for indicating equations on Linux.  However, for Windows, I had to use `\begin{equation}` and `\end{equation}`.  

# The Stack
* string.Template is used to render a markdown template  
* `pandas.DataFrame.to_markdown` is used to create markdown tables  
* `pandoc` is used to the convert markdown file output into a pdf file (markdown 🡲 LaTeX 🡲 pdf)  
* `browser-sync` (npm module) is used to run the `pantex.` version  

# The Files

### Input Files
* `mytemplate.md`  
* `mytemplate.pkl`  

### Output Files
* `_mytemplate.md` (rendered markdown)  
* `mytemplate.html` (in `edit` mode)  
* `mytemplate.pdf` (in `publish` mode)  
* `assets/` directory (containing images)  
