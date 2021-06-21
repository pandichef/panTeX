import os
from typing import Union
from typing_extensions import Literal
from string import Template
import pickle
import subprocess
from matplotlib.colors import BoundaryNorm
import pandas as pd
import seaborn as sns
import matplotlib

# the best image type for each file type
image_types = {"html": "png", "htm": "png", "pdf": "eps"}


class Manager:
    def __init__(
        self,
        template: Union[str, None] = None,
        context: Union[dict, str, None] = "context.pkl",
        assets_directory: str = "assets",
    ) -> None:
        self._template = template
        self._context = context
        self._assets_directory = assets_directory
        if isinstance(self._context, str):
            self._context_file_type = self._context.split(".")[-1]
        if not os.path.isdir(self._assets_directory):
            os.mkdir(self._assets_directory)

    def get_context(self):
        # if string, then it's serialized as pkl
        if isinstance(self._context, str):
            if self._context_file_type == "pkl":
                with open(self._context, "rb") as fn:
                    pickle_data = fn.read()
                return pickle.loads(pickle_data)
            else:
                raise Exception("Only .pkl context files are supported")
        else:
            return self._context

    def save_context(self, context_dict):
        # if string, then it's serialized as pkl
        if isinstance(self._context, str):
            if self._context_file_type == "pkl":
                with open(self._context, "wb") as fn:
                    fn.write(pickle.dumps(context_dict))
                return self._context  # return file name
            else:
                raise Exception("Only .pkl context files are supported")
        else:
            raise Exception(
                "Cannot save.  This Manager instance isn't using a pickled context file."
            )

    def _render_pandas_dataframe(self, df: pd.DataFrame, caption: str) -> str:
        md_string = df.to_markdown(index=False, numalign="center", stralign="center")
        # https://tex.stackexchange.com/questions/139106/referencing-tables-in-pandoc
        md_string += "\n\nTable: " + caption.replace("_", " ").title() + "\n\n"
        return md_string

    def _render_matplotlib_figure(  # and seaborn
        self,
        figure: Union[sns.axisgrid.FacetGrid, matplotlib.figure.Figure],
        caption: str,
        image_file_type: str,
    ) -> str:
        # returns a string, but ALSO saves the image to assets directory
        temp_file = (
            f"{self._assets_directory}/{caption.replace(' ','_')}.{image_file_type}"
        )
        figure.savefig(temp_file)
        md_string = f"![{caption.replace('_', ' ').title()}]({temp_file})"
        return md_string

    def _render_all_to_markdown(self, image_type: Literal["eps", "png"]):
        # stringified_context = self.get_context()
        # assert False, stringified_context is self.get_context()
        stringified_context = {}
        print(self.get_context())
        for label, value in self.get_context().items():
            if type(value) in [sns.axisgrid.FacetGrid, matplotlib.figure.Figure]:
                md_string = self._render_matplotlib_figure(value, label, image_type)
                stringified_context.update({label: md_string})
            elif type(value) == pd.DataFrame:
                md_string = self._render_pandas_dataframe(value, label)
                stringified_context.update({label: md_string})
            else:
                stringified_context.update({label: value})
        print(self._template)
        print(self._template)
        print(self._template)
        print(self._template)
        print(self._template)
        with open(self._template, "r") as fn:
            template_string = fn.read()
        print(stringified_context)
        template_object = Template(template_string)
        # safe_substitute allows you to include dollar signs
        rendered = template_object.safe_substitute(stringified_context)
        return rendered

    def _save_rendered_markdown_file(self, report_filename):
        split_filename = report_filename.split(".")
        report_file_extension = split_filename[-1]
        basename = ".".join(split_filename[:-1])
        markdown_filename = basename + ".md"
        with open(markdown_filename, "w") as fn:
            fn.write(self._render_all_to_markdown(image_types[report_file_extension]))
        return markdown_filename

    def save_to_pdf(self, report_filename) -> None:
        # converts markdown file to pdf file
        report_file_extension = report_filename.split(".")[-1]
        assert (
            report_file_extension == "pdf"
        ), "The report file name must have a pdf extension"
        markdown_filename = self._save_rendered_markdown_file(report_filename)
        subprocess.run(
            f"pandoc {markdown_filename} --pdf-engine xelatex -o {report_filename}",
            shell=True,
            check=True,
        )

    def _render_to_html_body(self, report_filename) -> str:
        # converts markdown file to html-body and then returns the body
        report_file_extension = report_filename.split(".")[-1]
        assert report_file_extension in [
            "html",
            "htm",
        ], "The report file name must have an html or htm extension"
        markdown_filename = self._save_rendered_markdown_file(report_filename)
        subprocess.run(  # markdown to html
            f"pandoc --toc --standalone --mathjax {markdown_filename} -o {report_filename}",
            shell=True,
            check=True,
        )
        with open(f"{report_filename}", "r") as fn:
            body_text = fn.read()
        return body_text

    def save_to_html(self, report_filename) -> None:
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
        body_text = self._render_to_html_body(report_filename)
        # print(body_text)
        rendered = html_template.substitute({"html_body": body_text})
        with open(f"{report_filename}", "w") as fn:
            fn.write(rendered)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--template",
        "-s",
        required=True,
        # default=os.getcwd(),
        # help="Specify alternative directory " "[default:current directory]",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        # default=os.getcwd(),
        # help="Specify alternative directory " "[default:current directory]",
    )
    args = parser.parse_args()

    # import numpy as np
    # import matplotlib.pyplot as plt

    # # Apply the default theme
    # sns.set_theme()

    # # Load an example dataset
    # df = sns.load_dataset("tips")

    # # Create a visualization
    # sns_plot = sns.relplot(
    #     data=df,
    #     x="total_bill",
    #     y="tip",
    #     col="time",
    #     hue="smoker",
    #     style="smoker",
    #     size="size",
    # )

    # np.random.seed(19680801)

    # # example data
    # mu = 100  # mean of distribution
    # sigma = 15  # standard deviation of distribution
    # x = mu + sigma * np.random.randn(437)

    # num_bins = 50

    # fig, ax = plt.subplots()

    # # the histogram of the data
    # n, bins, patches = ax.hist(x, num_bins, density=True)

    # # add a 'best fit' line
    # y = (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(
    #     -0.5 * (1 / sigma * (bins - mu)) ** 2
    # )
    # ax.plot(bins, y, "--")
    # ax.set_xlabel("Smarts")
    # ax.set_ylabel("Probability density")
    # ax.set_title(r"Histogram of IQ: $\mu=100$, $\sigma=15$")

    # fig.tight_layout()

    s = Manager(args.template)

    # s.save_context(
    #     {
    #         "customer_name": "J.P. Morgan Chase",
    #         "date_string": "March 2021",
    #         "the_raw_data": df.head(3),
    #         "image_file_name": sns_plot,
    #         "matplotlib1": fig,
    #     }
    # )

    # s.run_dev_server()
    s.save_to_pdf(args.output)
