# PyWLGK

Python implementation of the Weisfeiler-Lehman Graph Kernels (WLKs) method.
This package is an alternative to FastWLK, GraKel, and other implementations of the WLKs method.

## Installation

By design, PyWLGK is installable from PyPI and Anaconda. To install the package with `pip`, run the following command:

```bash
pip install pywlgk
```

or with `conda` (alternatively with `mamba` by replacing `conda` with `mamba`

```bash
conda install pywlgk
```

## Usage

PyWLGK is designed to be easy to use. The following example shows how to use PyWLGK to compute the WLKs kernel between 
two graphs.

```python
from pywlgk import wlk
import numpy as np

adjs = np.random.randint(0, 1, size=(2, 10, 10))
adjs = np.array(adjs + adjs.transpose(0, 2, 1), dtype=np.int32)
labels = np.ones((2, 10), dtype=np.int32)
wlk(adjs, labels, k=4)
```

PyWLGK takes as input a stack of adjacency matrices (`adjs`) and a stack of node labels (`labels`). The adjacency 
matrices must be symmetric, whereas the labels can have any type. Additionally, one can specify a `k` to control how 
many iterations of the kernel will be computed.
