# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ripley', 'ripley._clickhouse', 'ripley._sql_cmd', 'ripley.models']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ripley',
    'version': '0.dev129',
    'description': 'data / db manipulation',
    'long_description': '# Ripley\n\nAt one point in my work, I had many routine tasks related to various data manipulations and database structures. \nThese tasks were tied to analytics, legacy systems, research, recalculations, data transfers, pipelines, and simply \npoor planning and processes. I started this project just for fun. Maybe it will be useful to someone.\n\nThe package provides a simple interface for routine data operations. The main idea:\n\n- no dependencies\n- no error handlers and no package-specific errors\n- no loggers \n- isolation from the database driver\n\nSee [Latest Release Notes](https://d-ganchar.gitlab.io/ripley)\n\nSee [Wiki](https://gitlab.com/d-ganchar/ripley/-/wikis/home)',
    'author': 'Danila Ganchar',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<3.13',
}


setup(**setup_kwargs)
