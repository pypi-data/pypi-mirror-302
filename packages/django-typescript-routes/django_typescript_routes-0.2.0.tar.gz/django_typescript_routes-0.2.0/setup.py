# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typescript_routes',
 'typescript_routes.lib',
 'typescript_routes.management',
 'typescript_routes.management.commands']

package_data = \
{'': ['*'], 'typescript_routes': ['templates/*']}

install_requires = \
['Django>=5,<6']

setup_kwargs = {
    'name': 'django-typescript-routes',
    'version': '0.2.0',
    'description': 'Generate typescript routes from a Django URLconf',
    'long_description': '# django-typescript-routes\n\nMeant as a spiritual successor to [django-js-reverse](https://pypi.org/project/django-js-reverse/), `django-typescript-routes` is meant to answer to the following question:\n\n> I\'ve got a Typescript-based SPA that is powered by a Django-based API. How do I safely make requests to Django without messing up the routes or parameters?\n\n`django-typescript-routes` is how! At a high level, it turns:\n\n```python\nurls = [\n    path(\n        r"about",\n        about,\n        name="about",\n    ),\n    path(\n        r"/<str:username>",\n        subscribe,\n        name="subscribe",\n    ),\n    path(\n        r"/<str:username>/subscribers/<pk:uuid>/success",\n        subscription_success,\n        name="subscription-success",\n    ),\n]\n```\n\ninto:\n\n```typescript\nconst URLS = {\n  about: () => `/`,\n  subscribe: (username: string) => `/${username}`,\n  "subscription-success": (username: string, pk: string) =>\n    `/${username}/subscribers/${pk}/success`,\n};\n```\n\n## Quick start\n\n1. Install:\n\n```bash\npoetry add --dev django-typescript-routes\n```\n\n1. Add `django-typescript-routes` to your `INSTALLED_APPS` setting:\n\n```python\nINSTALLED_APPS = [\n    ...,\n    "typescript_routes",\n    ...\n]\n```\n\n2. Run the management command to print out the typescript file:\n\n```bash\npython manage.py generate_typescript_routes --urlconf projectname.urls > assets/urls.ts\n```\n\n## Contributing\n\n### Running the test suite\n\nSimply:\n\n```\n./scripts/test\n```\n',
    'author': 'Justin Duke',
    'author_email': 'justin@buttondown.email',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/buttondown-email/django-typescript-routes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
