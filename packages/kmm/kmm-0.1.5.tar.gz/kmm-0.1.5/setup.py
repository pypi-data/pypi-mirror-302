# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kmm', 'kmm.header', 'kmm.positions']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.2,<2.0.0',
 'pydantic>=2.0.0,<3.0.0',
 'sweref99==0.2']

setup_kwargs = {
    'name': 'kmm',
    'version': '0.1.5',
    'description': 'Minimalistic library for reading files in the kmm/kmm2 file format',
    'long_description': 'None',
    'author': 'NextML AB',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
