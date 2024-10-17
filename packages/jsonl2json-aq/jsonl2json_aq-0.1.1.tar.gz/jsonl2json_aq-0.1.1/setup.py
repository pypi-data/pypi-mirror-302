# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonl2json_aq']

package_data = \
{'': ['*']}

install_requires = \
['jsonlines>=4.0.0,<5.0.0']

entry_points = \
{'console_scripts': ['jl2j = jsonl2json_aq.__main__:main']}

setup_kwargs = {
    'name': 'jsonl2json-aq',
    'version': '0.1.1',
    'description': 'Converts jsonlines file to json file, by converting it into array of json objects.',
    'long_description': '# jsonl2json\n\nConverts jsonlines file to json file, by converting it into array of json objects.\n\n## Install\n\n###### Recommended (To install pipx click [here](https://github.com/pypa/pipx#install-pipx))\n\n```sh\npipx install jsonl2json-aq\n```\n\n###### or\n\n```sh\npip install jsonl2json-aq\n```\n\n#### Or upgrade by\n\n```sh\npipx upgrade jsonl2json-aq\n```\n\n###### or\n\n```sh\npip install --upgrade jsonl2json-aq\n```\n\n## Usage\n\n```sh\njl2j input_file output_file\n```\n\n## Install from source\n\nPoetry is required. For installation click [here](https://python-poetry.org/docs/#installation).\n\nDownload the source and install the dependencies by running:\n\n```sh\ngit clone https://github.com/aqdasak/jsonl2json.git\ncd jsonl2json\npoetry install\n```\n\n## License\n\nThis project is licensed under the MIT License.\n',
    'author': 'Aqdas Ahmad Khan',
    'author_email': 'aqdasak@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aqdasak/jsonl2json',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
