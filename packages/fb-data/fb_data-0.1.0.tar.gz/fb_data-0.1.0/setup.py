# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fb_data']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.32,<2.0',
 'google-api-python-client>=2.0,<3.0',
 'google-auth>=2.0,<3.0',
 'pandas>=1.3.0,<3.0',
 'snowflake-connector-python>=3.7.0,<4.0',
 'snowflake-sqlalchemy>=1.4.7,<2.0']

setup_kwargs = {
    'name': 'fb-data',
    'version': '0.1.0',
    'description': 'Python package with helper functions for the Data team.',
    'long_description': '# fb_data\n\nA Python package for working with Snowflake data.\n\n## Installation\n\nYou can install this package using pip:\n\n```\npip install git+https://github.com/yourusername/fb_data.git\n```\n\n## Usage\n\n```python\nfrom fb_data import Snowflake\n\n# Initialize Snowflake connection\nsf = Snowflake(\n    user="your_username",\n    password="your_password",\n    account=\'your_account\',\n    warehouse=\'your_warehouse\',\n    database=\'your_database\',\n    schema=\'your_schema\',\n    role=\'your_role\'\n)\n\n# Execute a query\nresult = sf.execute_query("SELECT * FROM your_table LIMIT 10")\n\n# Execute a query and get results as a DataFrame\ndf = sf.execute_query_to_dataframe("SELECT * FROM your_table LIMIT 10")\n\n# Write a DataFrame to Snowflake\nimport pandas as pd\ndf = pd.DataFrame(...)  # Your data here\nsf.write_dataframe_to_table(df, \'your_table\', if_exists=\'replace\')\n\n# Close the connection\nsf.close()\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.',
    'author': 'markostefanovic1',
    'author_email': 'marko.stefanovic@fishingbooker.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
