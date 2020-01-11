import re
import json
import sys
import shlex
import subprocess as sp
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import *

import nbformat

from nbconvert import MarkdownExporter
from nbconvert.preprocessors import Preprocessor

from traitlets.config import Config


########## Jupyter stuff #################

class CustomPreprocessor(Preprocessor):
    """Remove blank code cells and unnecessary whitespace."""

    def preprocess(self, nb, resources):
        """
        Remove blank cells
        """
        for index, cell in enumerate(nb.cells):
            if cell.cell_type == 'code' and not cell.source:
                nb.cells.pop(index)
            else:
                nb.cells[index], resources = self.preprocess_cell(cell, resources, index)
        return nb, resources

    def preprocess_cell(self, cell, resources, cell_index):
        """
        Remove extraneous whitespace from code cells' source code
        """
        if cell.cell_type == 'code':
            cell.source = cell.source.strip()

        return cell, resources


def doctor(string: str) -> str:
    """Get rid of all the wacky newlines nbconvert adds to markdown output and return result."""
    post_code_newlines_patt = re.compile(r'(```)(\n+)')
    inter_output_newlines_patt = re.compile(r'(\s{4}\S+)(\n+)(\s{4})')

    post_code_filtered = re.sub(post_code_newlines_patt, r'\1\n\n', string)
    inter_output_filtered = re.sub(inter_output_newlines_patt, r'\1\n\3', post_code_filtered)

    return inter_output_filtered


def notebook_to_markdown(path: Union[Path, str]) -> str:
    """
    Convert jupyter notebook to hugo-formatted markdown string
    Args:
        path: path to notebook
    Returns: hugo-formatted markdown
    """
    # first, update the notebook's metadata
    update_notebook_metadata(path)

    with open(Path(path)) as fp:
        notebook = nbformat.read(fp, as_version=4)
        assert 'front-matter' in notebook['metadata'], "You must have a front-matter field in the notebook's metadata"
        front_matter_dict = dict(notebook['metadata']['front-matter'])
        front_matter = json.dumps(front_matter_dict, indent=2)

    c = Config()
    c.MarkdownExporter.preprocessors = [CustomPreprocessor]
    markdown_exporter = MarkdownExporter(config=c)

    markdown, _ = markdown_exporter.from_notebook_node(notebook)
    doctored_md = doctor(markdown)
    # added <!--more--> comment to prevent summary creation
    output = '\n'.join(('---', front_matter, '---', '<!--more-->', doctored_md))

    return output


def write_hugo_formatted_nb_to_md(notebook: Union[Path, str], render_to: Optional[Union[Path, str]] = None) -> Path:
    """
    Convert Jupyter notebook to markdown and write it to the appropriate file.
    Args:
        notebook: The path to the notebook to be rendered
        render_to: The directory we want to render the notebook to
    """
    notebook = Path(notebook)
    notebook_metadata = json.loads(notebook.read_text())['metadata']
    rendered_markdown_string = notebook_to_markdown(notebook)
    slug = notebook_metadata['front-matter']['slug']
    render_to = render_to or notebook_metadata['hugo-jupyter']['render-to'] or 'content/post/'

    if not render_to.endswith('/'):
        render_to += '/'

    rendered_markdown_file = Path(render_to, slug + '.md')

    if not rendered_markdown_file.parent.exists():
        rendered_markdown_file.parent.mkdir(parents=True)

    rendered_markdown_file.write_text(rendered_markdown_string)
    print(notebook.name, '->', rendered_markdown_file.name)
    return rendered_markdown_file


def update_notebook_metadata(notebook: Union[Path, str],
                             title: Union[None, str] = None,
                             subtitle: Union[None, str] = None,
                             date: Union[None, str] = None,
                             slug: Union[None, str] = None,
                             render_to: str = None) -> Path:
    """
    Update the notebook's metadata for hugo rendering
    Args:
        notebook: notebook to have edited
    """
    notebook_path: Path = Path(notebook)
    notebook_data: dict = json.loads(notebook_path.read_text())
    old_front_matter: dict = notebook_data.get('metadata', {}).get('front-matter', {})

    # generate front-matter fields
    title = title or old_front_matter.get('title') or notebook_path.stem
    subtitle = subtitle or old_front_matter.get('subtitle') or 'Generic subtitle'
    date = date or old_front_matter.get('date') or datetime.now().strftime('%Y-%m-%d')
    slug = slug or old_front_matter.get('slug') or title.lower().replace(' ', '-')

    front_matter = {
        'title': title,
        'subtitle': subtitle,
        'date': date,
        'slug': slug,
    }

    # update front-matter
    notebook_data['metadata']['front-matter'] = front_matter

    # update hugo-jupyter settings
    render_to = render_to or notebook_data['metadata'].get('hugo-jupyter', {}).get('render-to') or 'content/post/'
    hugo_jupyter = {
        'render-to': render_to
    }
    notebook_data['metadata']['hugo-jupyter'] = hugo_jupyter

    # write over old notebook with new front-matter
    notebook_path.write_text(json.dumps(notebook_data))

    # make the notebook trusted again, now that we've changed it
    sp.run(['jupyter', 'trust', str(notebook_path)])

    return notebook_path