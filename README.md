# `proofread-eng-scify`, an ALM

An artisanal language model (ALM) for proofreading English prose in the
style of old-old-school science fiction, like Jules Verne, Lewis Carroll, and
L. Frank Baum. 

-----

## For someone who wants to use the proofreader

### Installation

```
uv add proofread-eng-scifi
```

or

```
pip install proofread-eng-scifi
```

### Using the proofreader

In a Python script

```
from proofread-eng-scifi.proof_## import proof_file
proof_file("text_file.txt")
```

or

```
from proofread-eng-scifi.proof_## import proof_text
proof_text(text_string)
```


-----

## For someone who wants to modify the proofreader

Get an editable copy installed

```
uv pip install -e proofread-eng-scifi
```
or

```
git clone https://codeberg.org/brohrer/proofread-eng-scifi.git
cd proofread-eng-scifi
uv pip install -e .
```

### Testing

From the top level project directory, run

```
uv run pytest
```

### Running evaluations

`uv run evals/eval_proofreading.py`

### How the code is organized

![Project structure for proofread-eng-scifi
](https://raw.githubusercontent.com/brohrer/blog_images/refs/heads/main/alms_task/project_structure.png)

Detail in [this blog post](https://brandonrohrer.at/alms_end_to_end.html).

## Publishing new versions to PyPI

Make sure to bump ther version number of necessary.

```
uv build
```

Set the test pypi token in the local environment with

```
export UV_PUBLISH_TOKEN=pypi-AgENdGVzdC5weXBp...
```

Publish a test version to PyPI test environment if desired

```
uv publish --publish-url https://test.pypi.org/legacy/
```

after testing, update `UV_PUBLISH_TOKEN` to the token for the primary
pypi environment and upload to PyPI

```
export UV_PUBLISH_TOKEN=pypi-AgENdGVzdC5weXBp...
uv publish
```


