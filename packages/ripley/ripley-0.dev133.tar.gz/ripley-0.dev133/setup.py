# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ripley', 'ripley._clickhouse', 'ripley._sql_cmd', 'ripley.models']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ripley',
    'version': '0.dev133',
    'description': 'data / database manipulation tool. See: https://gitlab.com/d-ganchar/ripley/-/pipelines/1498198176/',
    'long_description': '# Ripley\n\nAt one point in my life, I had many routine tasks related to various data manipulations and database structures. \nThese tasks were related to recalculations, one time data transfers / scripting / pipelines, legacy, research, \nanalytics etc. I started this package just for fun. Maybe it will be useful to someone.\n\nRipley provides a simple interface for routine data operations. The main idea:\n\n- no dependencies\n- no error handlers\n- no package errors\n- no loggers \n- isolation from the database driver\n\nSee [Latest Release Notes](https://d-ganchar.gitlab.io/ripley)\n\nSee [Wiki](https://gitlab.com/d-ganchar/ripley/-/wikis/home)',
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
