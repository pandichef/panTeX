# https://seaborn.pydata.org/introduction.html
import subprocess
from string import Template
from uuid import uuid4
import seaborn as sns

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

image_id = uuid4()
sns_plot.savefig(f"images/{image_id}.png")

###########################################################
# Generate markdown file
with open("markdown_template.md", "r") as fn:
    markdown_template = fn.read()

t = Template(markdown_template)
rendered = t.safe_substitute(  # safe_substitute allows you to include dollar signs
    {
        "customer_name": "J.P. Morgan Chase",
        "date_string": "March 2021",
        "df_head": df.head().to_markdown(
            index=False, numalign="center", stralign="center"
        ),  # note: numalign & stralign are parameters that are passed to the tabulate package
        "image_id": image_id,
    }
)

with open("output/output.md", "w") as fn:
    fn.write(rendered)
###########################################################
# Convert markdown to pdf
# Both Miktex (on Windows) and pandoc must be installed for this to work
# Miktex installs ~10 packages before this works
# https://docs.python.org/3/library/subprocess.html
# https://pandoc.org/demos.html
subprocess.run(
    "pandoc output/output.md --pdf-engine xelatex -o output/output.pdf",
    shell=True,
    check=True,
)
