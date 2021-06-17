# Computational Morphology with HFST

This repository contains the source code for the web course ”Computational Morphology with HFST”.

The web course is an adaptation of the teaching material of the course ”Computational Morphology”
taught by Mathias Creutz in the Master’s programme “Linguistic Diversity and Digital Humanities”
at the University of Helsinki. The original course and its exercises have been created by
Mathias Creutz and co-developed by Senka Drobac. Using an earlier version of the course material,
Erik Axelson has developed a Jupyter notebook interactive version.

The web course uses the same examples and exercises as the original course,
but HFST command line tools have been replaced with [HFST Python interface](https://pypi.org/project/hfst-dev/).


## Content

The course is divided into seven parts, corresponding to the original lectures 1–3 and 5–8.

1. Theories of morphology, generators and analyzers, lexc
2. Finite-state basics, xfst rules
3. Disambiguation, probabilities, finite-state networks summarized
4. (no tutorial for this lecture)
5. Guessers, stemmers, regular expressions in xfst
6. Twolc, two-level rules
7. Flag diacritics, non-concatenative morphology
8. Optimization of finite-state networks

First part is in `Lecture1/Lecture.ipynb`, second part in `Lecture2/Lecture.ipynb` and so on.
The source Python files are located in `Lecture1/src/Lecture.py`, `Lecture2/src/Lecture.py` and so on.

Running the examples requires [Jupyter software](https://jupyter.org/install) and Python packages
[hfst-dev](https://pypi.org/project/hfst-dev/) and [graphviz](https://pypi.org/project/graphviz/).

The course material and the examples themselves are visible also in Github. For example, if you wish
to see Lecture1, just go to the directory `Lecture1` and click the `Lecture.ipynb` file. Github will
show it as it will be shown when run with Jupyter.


## More info

For more information about the course, including licensing and preferred citation,
see the [info](http://urn.fi/urn:nbn:fi:lb-2021053003) and
[MetaShare](http://urn.fi/urn:nbn:fi:lb-2021053001) pages.
