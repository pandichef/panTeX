# panTeX
Generating pretty reports using pandas and matplotlib.  

# Installation
* `pip install pantex` to install the main application  
* Install [MiKTeX](https://miktex.org/howto/install-miktex) (on Windows) or TBD on Linux  
* Install [pandoc](https://pandoc.org/installing.html)  
* Install [Browsersync](https://browsersync.io/) (for browser mode): `npm install -g browser-sync`  

# Quickstart
To create a `pantex.Manager` object:  
```python
m = pantex.Manager('mytemplate.md')
```  

To save context to `mytemplate.pkl`: 
```python
m.save_context({'my_header': 'Hello World!', 'my_table': df.head()})
```

To append to context in a Python script:  
```python
m.save_context({'my_footer': 'Goodbye!', 'an_image': mplFigure}, append=True)
```

To generate a pretty pdf report:  
```python
m.save_to_pdf()
```

To read the current context in a Python script: `m.get_context()`  
```python
m.get_context()
```

# Quickstart via Command Line
To run in browser mode: `python -m pantex.edit mytemplate.md`  
To prduce a pretty LaTeX pdf report: `python -m pantex.publish mytemplate.md`  

# How it works
Inspired by traditional website rendering, a report generation process is divided into two parts:  
1. A markdown template with [Python-native template variables](https://docs.python.org/3/library/string.html#template-strings).  
1. A context dictionary, which is saved at `mytemplate.pkl`  

For example, say you have a markdown file at `./mytemplate.md`, containing:
```markdown
# ${my_header}
${my_table}
Some text
```

In Python, you can write:  
```python
m = pantex.Manager('mytemplate.md')
m.save_context({'my_header': 'Hello World!', 'my_table': df.head()})
m.save_to_pdf()
```

panTeX will combine the markdown template and the Python context and produce a pretty pdf LaTeX report. 
Note that pandas DataFrame objects will be automatically rendered as a table.  Matplotlib/Seaborn 
charts and LaTeX style equations are also supported.  (The LaTeX equations must be contained in `\begin{equation}`/`\end{equation}` tags.)

# The Development Server (Edit Mode)
`python -m pantex.edit mytemplate.md` enables an in-browser version of the LaTeX report.  It's not quite as pretty as the pdf version, but it offers a near real time rendering experience.  (Rendering of pdf reports is typically too slow for editing.) If you need 
the html files, they can be found at `mytemplate.html` and `assets/`.
