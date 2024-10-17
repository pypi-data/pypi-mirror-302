# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsafe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tsafe',
    'version': '1.0.0',
    'description': 'A module that forces functions to be type safe.',
    'long_description': '# TSafe\nA module that forces functions to be type safe.\n\n![PyPI - Version](https://img.shields.io/pypi/v/tsafe)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tsafe)\n![PyPI - License](https://img.shields.io/pypi/l/tsafe)\n\n## Table of Contents\n* [Install](#install)\n* [Quick Start](#quick-start)\n* [Docs](#docs)\n* [Contributing](#contributing)\n\n## Install\nTo install TSafe use `pip`.\n```\npip3 install tsafe\n```\n\n## Quick Start\nTo get started with TSafe first import functions from `tsafe` into your project like this.\n```py\nfrom tsafe import FUNCTIONS_HERE\n```\n\nTo find out what to import, and how to use TSafe check out the [docs](#docs).\n\n\n## Docs\n\n### type_safe/safe\nWrapper function to force a function to be type safe\n\nUssage:\n```py\nfrom tsafe import type_safe\n\n@type_safe # or @safe\ndef hello_x(x: str):\n    print("Hello " + x)\n\nhello_x("World")\n# works normally\n# output: "Hello World"\n\nhello_x(10)\n# throws error since int is not type str\n# output: Exception: argument 12 is not type of <class \'str\'>\n\n```\n\n## Contributing\nAll types of contibutions are welcome for the TSafe project, whether its updating the documentation, reporting issues, or simply mentioning TSafe in your projects.\n\nRemember this before contibuting, you should open an **Issue** if you don\'t think you can contribute and open a **Pull Request** if you have a patch for an issue.\n\n\n\n### Reporting Bugs\nBefore you submit a bug report make sure you have the following information or are using the following things.\n\n* Make sure you\'re on the latest version.\n* Make sure its not just on your end (if you were possibly using a python version we dont support).\n* Check issues to see if it has already been reported.\n* Collect the following info about the bug:\n    * Stack Trace.\n    * OS, Platform and Version (Windows, Linux, macOS, x86, ARM).\n    * Possibly your input and the output.\n    * Can you reliably reproduce the issue?\n\nIf you have all of that prepared you are more than welcome to open an issue for the community to take a look at.',
    'author': 'Ethan Illingsworth',
    'author_email': 'illingsworth.ethan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
