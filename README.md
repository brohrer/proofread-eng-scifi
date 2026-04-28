# `proofread-eng-scify`, an ALM

An artisanal language model (ALM) for proofreading English prose in the
style of old-old-school science fiction, like Jules Verne, Lewis Carroll, and
L. Frank Baum. 

-----

## For someone who wants to use the proofreader

### Installation

### Using the proofreader

##

-----

## For someone who wants to modify the proofreader

### Testing

From the top level project directory, run

```
uv run pytest
```

### Running evaluations

`evals/`

### How the code is organized

**Model development code** sits in the top level `model_dev/` directory. Once
models have been created and tested and are ready to be used in the
proofreader, they are moved to the `src/proofread_eng_scify/models/`
directory. Versions are indicated with a two digit squential counter
appended to the model name, such as `tokenizer_13`.


**Tests** are scattered throughout the code, sitting close to the code they are
meant to test. They are primarily unit tests. For now, integration and
end-to-end testing gets covered by evaluations.

**Evaluations** are in `evals/`

