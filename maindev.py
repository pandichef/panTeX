# https://seaborn.pydata.org/introduction.html
from datetime import time
import subprocess
from string import Template
from uuid import uuid4
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# https://latex.vercel.app/
html_template = Template(
    """
    <!DOCTYPE html>
    <html>
        <head>
            <link rel="stylesheet" href="https://latex.now.sh/style.css">
            <link rel="stylesheet" href="https://latex.now.sh/prism/prism.css">
        </head>
    <body>
    ${html_body}
    <script type="text/javascript" id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
    </script>
    <script src="https://cdn.jsdelivr.net/npm/prismjs/prism.min.js"></script>
    <script id="__bs_script__">//<![CDATA[
        document.write("<script async src='http://HOST:3000/browser-sync/browser-sync-client.js?v=2.26.14'><\/script>".replace("HOST", location.hostname));
    //]]></script>
    </body>
    </html>
    """
)

# html/htm types not yet fully supported
def render_markdown(template_name, report_name, context=None):
    image_types = {"html": "png", "htm": "png", "pdf": "eps"}
    assets_directory = "assets"
    report_type = report_name.split(".")[-1]
    image_file_type = image_types[report_type]

    print("asdf")
    try:
        subprocess.run(f"mkdir {assets_directory}", shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"mkdir {assets_directory}: directory already exists")

    ###########################################################
    # Generate markdown file
    with open(template_name, "r") as fn:
        markdown_template = fn.read()

    for key, value in context.items():
        if type(value) in [sns.axisgrid.FacetGrid, matplotlib.figure.Figure]:
            # image_id = uuid4()
            temp_file = f"{assets_directory}/{key.replace(' ','_')}.{image_file_type}"
            value.savefig(temp_file)
            md_string = f"![{key.replace('_', ' ').title()}]({temp_file})"
            context.update({key: md_string})
        elif type(value) == pd.DataFrame:
            md_string = value.to_markdown(
                index=False, numalign="center", stralign="center"
            )
            # https://tex.stackexchange.com/questions/139106/referencing-tables-in-pandoc
            md_string += "\n\nTable: " + key.replace("_", " ").title() + "\n\n"
            context.update({key: md_string})
        # print(context[key])

    # note: numalign & stralign are parameters that are passed to the tabulate package
    t = Template(markdown_template)
    # safe_substitute allows you to include dollar signs
    rendered = t.safe_substitute(context)

    # print(rendered)
    with open(f"./{assets_directory}/output.md", "w") as fn:
        fn.write(rendered)

    ###########################################################
    # Convert markdown to pdf
    # Both Miktex (on Windows) and pandoc must be installed for this to work
    # Miktex installs ~10 packages before this works
    # https://docs.python.org/3/library/subprocess.html
    # https://pandoc.org/demos.html
    if report_type == "pdf":
        subprocess.run(
            f"pandoc {assets_directory}/output.md --pdf-engine xelatex -o {report_name}",
            shell=True,
            check=True,
        )
    elif report_type in ["html", "htm"]:
        # https://stackoverflow.com/questions/37533412/md-with-latex-to-html-with-mathjax-with-pandoc
        subprocess.run(
            f"pandoc --toc --standalone --mathjax {assets_directory}/output.md -o {report_name}",
            shell=True,
            check=True,
        )
        with open(f"{report_name}", "r") as fn:
            body_text = fn.read()
        if report_type in ["html", "htm"]:
            rendered = html_template.substitute({"html_body": body_text})
        with open(f"{report_name}", "w") as fn:
            fn.write(rendered)
    else:
        raise Exception(f"Report type {report_type} not supported!")

    # Cleanup temporary files
    # subprocess.run("rm -rf ./temporary_files", shell=True, check=True)

    return True


# Apply the default theme
sns.set_theme()

# Load an example dataset
df = sns.load_dataset("tips")

# Create a visualization
sns_plot = sns.relplot(
    data=df,
    x="total_bill",
    y="tip",
    col="time",
    hue="smoker",
    style="smoker",
    size="size",
)


np.random.seed(19680801)

# example data
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution
x = mu + sigma * np.random.randn(437)

num_bins = 50

fig, ax = plt.subplots()

# the histogram of the data
n, bins, patches = ax.hist(x, num_bins, density=True)

# add a 'best fit' line
y = (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2)
ax.plot(bins, y, "--")
ax.set_xlabel("Smarts")
ax.set_ylabel("Probability density")
ax.set_title(r"Histogram of IQ: $\mu=100$, $\sigma=15$")

fig.tight_layout()

from devserver import check_for_updates


def run_dev_server():
    previous_hash = None
    browser_sync_process = subprocess.Popen(
        'browser-sync start --server --files "*.html" --index "output.html',
        shell=True,
        # check=True,
    )
    print("BrowserSync PID: ", browser_sync_process.pid)
    while True:
        # subprocess.Popen
        new_hash = check_for_updates(
            filename="./markdown_template.md", previous_hash=previous_hash
        )

        render_markdown(
            "markdown_template.md",
            "output.html",
            {
                "customer_name": "J.P. Morgan Chase",
                "date_string": "March 2021",
                "the_raw_data": df.head(3),
                "image_file_name": sns_plot,
                "matplotlib1": fig,
            },
        )
        # print("dfh")

        previous_hash = new_hash


def convert_to_pdf():
    render_markdown(
        "markdown_template.md",
        "output.pdf",
        {
            "customer_name": "J.P. Morgan Chase",
            "date_string": "March 2021",
            "the_raw_data": df.head(3),
            "image_file_name": sns_plot,
            "matplotlib1": fig,
        },
    )


run_dev_server()
