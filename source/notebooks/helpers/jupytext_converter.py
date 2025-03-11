"""
No edits are expected to be made here
This is the main function to convert python and Rmd files
into ipynb and execute them with given parameters
"""

import os
import pathlib
import tempfile
from typing import Literal

import jupytext
import nbconvert
import nbformat
import papermill as pm

from .config import PY_KERNEL_NAME, R_KERNEL_NAME, NOTEBOOK_DIR


def convert_file_and_run_ipynb(
    notebooks: list,
    output_dir: pathlib.PosixPath,
    parameters: dict,
    language: Literal["R", "python"] = "python",
    save_html: bool = True,
):
    """Convert py notebook files to ipynb and execute with papermill

    Args:
        notebooks (list): notebook filenames to run in the given order
        output_dir (pathlib.PosixPath): should be the OUTPUT_DIR defined in papermill.ipynb
        parameters (dict): parameters to pass to papermill
        language (str): 'python' or 'R'
        save_html (bool): save papermill output as HTML, if False then save as ipynb. Default to True.
    """
    if language == "python":
        kernel = PY_KERNEL_NAME
        file_type = "ipynb"
    elif language == "R":
        kernel = R_KERNEL_NAME
        file_type = "Rmd"

    executed_ipynb_files = []

    with tempfile.TemporaryDirectory() as temp_dir:
        for filename in notebooks:
            print(f"Executing notebook: {filename}")
            
            notebook = convert_file_to_ipynb(filename, file_type=file_type)
            temp_ipynb_filename = f"{os.path.splitext(filename)[0]}.ipynb"
            temp_ipynb_file_path = os.path.join(temp_dir, temp_ipynb_filename)
            write_ipynb_tempdir(temp_dir=temp_ipynb_file_path, notebook=notebook)

            output_ipynb_file_path = os.path.join(output_dir, temp_ipynb_filename)

            pm.execute_notebook(
                temp_ipynb_file_path,
                output_ipynb_file_path,
                kernel_name=kernel,
                language=language,
                report_mode=False,
                parameters=parameters,
            )

            executed_ipynb_files.append(output_ipynb_file_path)

            if save_html:
                convert_ipynb_to_html(output_ipynb_file_path, output_dir)

    return executed_ipynb_files


def convert_file_to_ipynb(
    filename: str | pathlib.PosixPath, file_type: Literal["Rmd", "ipynb"]
) -> nbformat.notebooknode.NotebookNode:
    """Convert notebook py or rmd file to ipynb

    Args:
        filename (str): expected to be in source/notebooks/

    Returns:
        nbformat.notebooknode.NotebookNode: dictionary/json representation of ipynb
    """
    if type(filename) == str:
        py_file_path = str(NOTEBOOK_DIR / filename)
    else:
        py_file_path = filename

    try:
        with open(py_file_path, "r") as py_file:
            py_content = py_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {py_file_path}")
    else:
        file_type_map = {"Rmd": "Rmd", "ipynb": "ipynb"}

        fmt = file_type_map[file_type]

        return jupytext.reads(py_content, fmt=fmt)


def convert_ipynb_to_html(ipynb_file_path: str, output_dir: str) -> str:
    """Convert an executed ipynb notebook to HTML and save it.

    Args:
        ipynb_file_path: The path to the executed ipynb file.
        output_dir: Directory where the HTML file should be saved.

    Returns:
        The path to the saved HTML file.
    """
    html_exporter = nbconvert.HTMLExporter()
    html_output, _ = html_exporter.from_filename(ipynb_file_path)

    html_filename = f"{os.path.splitext(os.path.basename(ipynb_file_path))[0]}.html"
    html_file_path = os.path.join(output_dir, html_filename)

    print(f"Saving output to {html_filename}")
    with open(html_file_path, "w") as f:
        f.write(html_output)

    return html_file_path


def write_ipynb_tempdir(
    temp_dir: tempfile.TemporaryDirectory, notebook: nbformat.notebooknode.NotebookNode
):
    """Write ipynb to temporary directory so it can be read by papermill
    The TemporaryDirectory will be cleaned up after this run finishes and we will
    only be left with a ipynb file in the output directory

    Args:
        temp_dir: temp_dir to temporary write file to
        notebook: ipynb file created with convert_py_to_ipynb
    """
    with open(temp_dir, "w") as ipynb_file:
        nbformat.write(notebook, ipynb_file)

