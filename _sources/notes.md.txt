# Notes on production

This book is written with a combination of "markdown" text and
[Jupyter](https://www.jjupyter.org) notebooks to allow executable
content. It was then assembled using [Jupyter
Book](https://jupyterbook.org), and hosted on [GitHub
Pages](https://pages.github.com/).  All text, code, diagrams, and
generated datasets are available for download from [the project's
GitHub repo](https://github.com/simoninireland/introduction-to-epidemics).

Simulations are all written in [Python 3](https://www.python.org) and
expressed using the
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
datasets. The large experiments used a compute cluster ("`hogun`")
with 11 machines each with 16Gb of memory and two 4-core Intel Xeon
E3-1240@3.4MHz processors; all other experiments were performed on a
2017-vintage MacBook Pro with 16Gb of memory and a dual-core Intel
i5@3.1GHz processor.  


