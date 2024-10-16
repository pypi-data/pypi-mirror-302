# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wikipedia']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.12,<5.0',
 'pandas>=2.1.4,<3.0.0',
 'poetry>=1.1',
 'requests>=2.30.0,<3.0.0']

setup_kwargs = {
    'name': 'nlpia2_wikipedia',
    'version': '1.5.18',
    'description': 'Updated version of `wikipedia` package because original repo has been abandoned since 2014.',
    'long_description': '# Wikipedia\n\n<!-- [![image](https://travis-ci.org/goldsmith/Wikipedia.png?branch=master)](https://travis-ci.org/goldsmith/nlpia2-wikipedia) -->\n\n[![image](https://pypip.in/d/nlpia2-wikipedia/badge.png)](https://crate.io/packages/nlpia2-wikipedia)\n\n[![image](https://pypip.in/v/nlpia2-wikipedia/badge.png)](https://crate.io/packages/nlpia2-wikipedia)\n\n[![License](https://pypip.in/license/nlpia2-wikipedia/badge.png)](https://pypi.python.org/pypi/nlpia2-wikipedia/)\n\n**NLPiA2-Wikipedia** Thin Python wrapper for Wikipedia API\n\nSearch Wikipedia, get article summaries, get data like links and images\nfrom a page, and more. Wikipedia wraps the [MediaWiki API](https://www.mediawiki.org/wiki/API) so you can focus on using\nWikipedia data, not getting it.\n\n```python\n>>> from wikipedia import wikipedia as wiki\n>>> print wiki.summary("Wikipedia")\nWikipedia (/ˌwɪkɨˈpiːdiə/ or /ˌwɪkiˈpiːdiə/ WIK-i-PEE-dee-ə) is a collaboratively edited, multilingual, free Internet encyclopedia supported by the non-profit Wikimedia Foundation...\n\n>>> wiki.search("Barack")\n[\'Barak (given name)\', \'Barack Obama\', ... \'Presidential transition of Barack Obama\']\n>>> titles = wiki.search("New York")\n>>> page = wiki.page(titles[1])\n>>> page.title\n\'New York (State)\'\n>>> page.url\n\'http://en.wikipedia.org/wiki/New_York_(state)\'\n>>> page.content\n\'New York, sometimes called New York State...\'\n>>> page.summary\n\'New York, sometimes called New York State...\'\n>>> page.links[0]\n\'10 Hudson Yards\'\n\n>>> wiki.set_lang("fr")\n>>> wiki.summary("Facebook", sentences=1)\nFacebook est un service de réseautage social en ligne sur Internet permettant d\'y publier des informations (photographies, liens, textes, etc.) en contrôlant leur visibilité par différentes catégories de personnes.\n```\n\n(or one of the other more advanced [Python MediaWiki API\nwrappers](http://en.wikipedia.org/wiki/Wikipedia:Creating_a_bot#Python)),\nwhich has a larger API, rate limiting, and other features so we can be\nconsiderate of the MediaWiki infrastructure.\n\n## Installation\n\nTo install Wikipedia, simply run:\n\n    $ pip install nlpia2-wikipedia\n\nWikipedia is compatible with Python 2.6+ (2.7+ to run unittest discover)\nand Python 3.3+.\n\n## Documentation\n\nRead the docs at <https://wikipedia.readthedocs.org/en/latest/>.\n\n-   [Quickstart](https://wikipedia.readthedocs.org/en/latest/quickstart.html)\n-   [Full API](https://wikipedia.readthedocs.org/en/latest/code.html)\n\nTo run tests, clone the [repository on\nGitHub](https://github.com/goldsmith/Wikipedia), then run:\n\n    $ pip install -r requirements.txt\n    $ bash runtests  # will run tests for python and python3\n    $ python -m unittest discover tests/ \'*test.py\'  # manual style\n\nin the root project directory.\n\nTo build the documentation yourself, after installing requirements.txt,\nrun:\n\n    $ pip install sphinx\n    $ cd docs/\n    $ make html\n\n## License\n\nMIT licensed. See the [LICENSE\nfile](https://github.com/goldsmith/Wikipedia/blob/master/LICENSE) for\nfull details.\n\n## Credits\n\n- [Wikipedia](https://pypi.org/project/wikipedia)\n- [Pywikipediabot](http://www.mediawiki.org/wiki/Manual:Pywikipediabot)\n- [wiki-api](https://github.com/richardasaurus/wiki-api) by \\@richardasaurus\n- [Wikimedia Foundation](http://wikimediafoundation.org/wiki/Home) for giving the world free access to knowledge\n\n',
    'author': 'Hobson Lane',
    'author_email': 'hobson@tangibleai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/tangibleai/community/nlpia2-wikipedia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
