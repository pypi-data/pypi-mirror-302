# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rich2md']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.2.3,<3.0.0', 'rich>=13.9.2,<14.0.0']

setup_kwargs = {
    'name': 'rich2md',
    'version': '0.1.0',
    'description': 'Convert Rich tables to Markdown tables',
    'long_description': '# Rich2MD\n\nThis is a simple tool to convert [Rich](https://github.com/Textualize/rich) tables to Markdown tables.\n\n## Installation\n\n```bash\npip install rich2md\n```\n\n## Usage\n\nThere are two functions:\n\n- `rich_table_to_df` – converts the Rich `Table` object to a Pandas DataFrame.\n- `rich_table_to_md_table` – converts the Rich `Table` object to a Markdown table and returns it as a string.\n\nExample:\n\n```python\nfrom rich.table import Table\nfrom rich2md import rich_table_to_md_table\n\ntable = Table("A", "B")\ntable.add_row("my", "mom")\ntable.add_row("your", "dad")\ntable_md = rich_table_to_md_table(table)\nprint(table_md)\n```\n',
    'author': 'Krzysztof J. Czarnecki',
    'author_email': 'kjczarne@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
