# pretty-reports
Generating pretty reports using pandas and matplotlib.  

# Installation
* `pip install pretty-reports` to install the main application  
* Install [MiKTeX](https://miktex.org/howto/install-miktex) (on Windows) or TBD on Linux  
* Install [pandoc](https://pandoc.org/installing.html)  
* Install `browser-sync` (for browser mode): `npm install -g browser-sync`  

# Quickstart via Command Line
To run in browser mode: `pretty-reports --browser ./my_template_file.md`  
To prduce a pretty LaTeX pdf report: `pretty-reports ./my_template_file.md`  
To export context variables in a Python script: `save_context({'title': 'Hello World', 'table': df.head()})`  
To add to context in a Python script: `save_context({'title': 'Hello World', 'table': df.head()}, append=True)`  
To read the current context in a Python script: `read_context()`  

# Quickstart via Python
You can also use pantex directly from Python e.g., if you have a business process that pulls data from 
various sources and summarizes it in a LaTeX pdf document.  


# How it works
Inspired by traditional website rendering, a report generation process is divided into two parts:  
1. A markdown template with [Python-native template variables](https://docs.python.org/3/library/string.html#template-strings).  
1. A context dictionary, which is saved at `./assets/context.pkl`  

For example, say you have a markdown file at `./my_template.md`, containing:
```markdown
# ${my_header}
${my_table}
Some text
```

In Python, you can write:  
```python
save_context({'my_header': 'Hello World!', 'my_table': df.head()})
```

`pretty-reports` will combine the markdown template and the Python context and produce a pretty pdf LaTeX report. 
Note that pandas DataFrame objects will be automatically rendered as a table.  Matplotlib/Seaborn 
charts and LaTeX style equations are also supported.  (The LaTeX equations must be contained in `\begin{equation}`/`\end{equation}` tags.)

# The Development Server
`pretty-reports --browser` enables an in-browser version of the LaTeX report.  It's not quite as pretty as the pdf version, but 
it offers a near real time rendering experience.  Rendering pdf reports takes a bit more time.

# Notes

*  I had to add `*.md` to `.prettierignore`.  `LaTeX` equations were getting inappropriately edited in vscode.  
*  `$$` works for indicating equations on Linux.  However, for Windows, I had to use `\begin{equation}` and `\end{equation}`.  

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

# The Stack
* string.Template is used to render a markdown template  
* `pandas.DataFrame.to_markdown` is used to create markdown tables  
* `pandoc` is used to the convert markdown file output into a pdf file (markdown 🡲 LaTeX 🡲 pdf)  
* `browser-sync` (npm module) is used to run the `--browser` version  

# Requirements  
* See `requirements.txt` for the Python package requirements  
* Also requires `pandoc` and `MiKTeX` to be installed (on Windows)  
* `browser-sync` is required for `--dev` mode  

# Workflow
* Develop the document using a web page using `browser-sync start --server --files "*.html" --index "output.html"`  
* Print to `pdf` when you're ready  
