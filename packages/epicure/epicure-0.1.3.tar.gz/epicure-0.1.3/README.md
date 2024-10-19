# EpiCure

[![License BSD-3](https://img.shields.io/pypi/l/epicure.svg?color=green)](https://gitlab.pasteur.fr/gletort/epicure/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/epicure.svg?color=green)](https://pypi.org/project/epicure)
[![Python Version](https://img.shields.io/pypi/pyversions/epicure.svg?color=green)](https://python.org)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/epicure)](https://napari-hub.org/plugins/epicure)

Napari plugin to manually correct epithelia segmentation in movies

 > **Documentation in the [wiki](https://gitlab.pasteur.fr/gletort/epicure/-/wikis/EpiCure)**

## Installation

### Install plugin
To install EpiCure on a fresh python virtual environment, type inside the environement:
```
pip install epicure
``` 

Then launch `Napari`, and the plugin should be visible in the `Plugins` list.

If you already have an environment with `Napari` installed, you can also install it directly in `Napari>Plugins>Install/Uninstall plugins`

### Install code
To have the code to be able to modify it, clone this repository. You can use `pip install -e .` so that everytime you update the code, the plugin will be updated. 

## Usage

Refer to the [wiki](https://gitlab.pasteur.fr/gletort/epicure/-/wikis/EpiCure) for documentation of the different steps possible in the pipeline.



This [napari] plugin was initialized with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[file an issue]: https://github.com/gletort/epicure/issues
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
