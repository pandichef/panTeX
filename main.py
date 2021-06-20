# https://seaborn.pydata.org/introduction.html
from datetime import time
import subprocess
from string import Template
from uuid import uuid4
import seaborn as sns
import pandas as pd


def render_markdown(template_name, report_name, context=None):
    image_file_type = "eps"

    try:
        subprocess.run("mkdir temporary_files", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("mkdir temporary_files: directory already exists")

    ###########################################################
    # Generate markdown file
    with open(template_name, "r") as fn:
        markdown_template = fn.read()

    for key, value in context.items():
        if type(value) == sns.axisgrid.FacetGrid:
            image_id = uuid4()
            temp_file = f"./temporary_files/{image_id}.{image_file_type}"
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

    with open("temporary_files/output.md", "w") as fn:
        fn.write(rendered)

    ###########################################################
    # Convert markdown to pdf
    # Both Miktex (on Windows) and pandoc must be installed for this to work
    # Miktex installs ~10 packages before this works
    # https://docs.python.org/3/library/subprocess.html
    # https://pandoc.org/demos.html
    subprocess.run(
        f"pandoc temporary_files/output.md --pdf-engine xelatex -o {report_name}",
        shell=True,
        check=True,
    )

    # Cleanup temporary files
    subprocess.run("rm -rf ./temporary_files", shell=True, check=True)

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

render_markdown(
    "markdown_template.md",
    "output.pdf",
    {
        "customer_name": "J.P. Morgan Chase",
        "date_string": "March 2021",
        "the_raw_data": df.head(3),
        "image_file_name": sns_plot,
    },
)
