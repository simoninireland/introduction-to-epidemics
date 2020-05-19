# Notes on production

This book is written with a combination of "markdown" text and
[Jupyter](https://www.jjupyter.org) notebooks to allow executable
content. It was then assembled using [Jupyter
Book](https://jupyterbook.org), and hosted on [GitHub
Pages](https://pages.github.com/).  All text, code, diagrams, and
generated datasets are available for download from [the project's
GitHub repo](https://github.com/simoninireland/introduction-to-epidemics).

Simulations are all expressed using the
[`epydemic`](https://pyepydemic.readthedocs.io/en/latest/) library for
network simulation, which is itself built on top of the
[`networkx`](https://networkx.github.io/) library for representing and
manipulating networks in Python.

The mathematics makes heavy use of the [`numpy`](https://numpy.org/).
The diagrams are all generated using
[`matplotlib`](https://matplotlib.org/) together with
[`seaborn`](https://seaborn.pydata.org/) to improve the graphical
presentation, as well as some of the network visualisation functions
built into `networkx`.

For the experiments with a lot of numbers crunched we use the
[`epyc`](https://epyc.readthedocs.io/en/latest/) computational
experiment management library and
[`pandas`](https://pandas.pydata.org/) to handle the resulting
datasets. The experiments used our local compute cluster ("`hogun`"):
11 machines each with 16Gb of memory and 2 4-core Intel Xeon
E3-1240@3.4MHz processors.


