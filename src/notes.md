# Notes on production

Writing this book has meant bringing together text, mathematics, and
code, using a large array of open-source tools. It's amazing what you
can get your hands on these days, and I'm grateful to the contributors
to the various projects for their creativity and generosity.

The book is written with a combination of "markdown" text and
[Jupyter](https://www.jjupyter.org) notebooks to allow executable
content. It was then assembled using [Jupyter
Book](https://jupyterbook.org) to drive the
[Sphinx](https://www.sphinx-doc.org/en/master/) documentation generator,
and hosted on [GitHub Pages](https://pages.github.com/).

```{only} latex

The book is typeset by letting Sphinx drive the LaTeX typesetting
system. The style is based on Edward Tufte's books on scientific
visualisation, as implemented by the [Tufte-LaTeX
Developers](http://www.latextemplates.com/template/tufte-style-book).
```

Simulations are all written in [Python 3](https://www.python.org) and
expressed using the
[`epydemic`](https://pyepydemic.readthedocs.io/en/latest/) library for
network simulation, which itself is built on top of the
[`networkx`](https://networkx.github.io/) library for representing and
manipulating networks in Python.

The mathematics makes heavy use of the [`numpy`](https://numpy.org/).
The diagrams are all generated using
[`matplotlib`](https://matplotlib.org/) together with
[`seaborn`](https://seaborn.pydata.org/) to improve the graphical
presentation, as well as some of the network visualisation functions
built into `networkx`.

For the experiments where a lot of numbers are being crunched we use
the [`epyc`](https://epyc.readthedocs.io/en/latest/) computational
experiment management library and
[`pandas`](https://pandas.pydata.org/) to handle the resulting
datasets. The large experiments use a compute cluster ("`hogun`")
with 11 machines each with 16Gb of memory and two 4-core Intel Xeon
E3-1240@3.4MHz processors; all other experiments are performed on a
2017-vintage MacBook Pro with 16Gb of memory and a dual-core Intel
i5@3.1GHz processor.

All text, code, and diagrams are available for download from [the
project's GitHub
repo](https://github.com/simoninireland/introduction-to-epidemics).

