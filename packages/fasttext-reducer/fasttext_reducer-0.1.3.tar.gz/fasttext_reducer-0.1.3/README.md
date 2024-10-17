# fasttext-reducer
A tiny package (and standalone script) for downloading any pretrained fasttext word vector model to any desired location and then reducing its number of dimensions.

## Installation
Either run the following to install from PyPI:
```
pip install fasttext-reducer
```

Or clone the repository and install the package using `pip install .`

## Example usage
To download the English pretrained model, reduce it to 30 dimensions, and save it to `/Users/admin/`, you can run the following command:
```
fasttext-reduce --root_dir /Users/admin --lang en --dim 30
```
You can also use the package within Python:
```
from fasttext_reducer.reduce_fasttext_models import reduce_fasttext_models

reduce_fasttext_models('/Users/admin', 'en', 30)
```
