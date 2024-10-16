# LImA 2 Client library

This project provides a Python interface to the LImA 2 distributed system.

Checkout the [documentation here](https://limagroup.gitlab-pages.esrf.fr/lima2-client/).

### Bootstrapping the documentation

The source for the documentation is in the `docs` folder. Here are the instructions to built and read it locally. The documentation is built with [Doxygen](http://www.doxygen.org/) and [Sphinx](http://www.sphinx-doc.org). The sphinx template is from [Sphinx Material](https://bashtage.github.io/sphinx-material/).

```
    conda create -n doc --file docs/requirements.txt -c conda-forge
    conda activate doc
    cd docs  
    make html
```

The html documentation is generated in `docs/.build/html`.
