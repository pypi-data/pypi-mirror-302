# fb_data

A Python package for working with Snowflake data.

## Installation

You can install this package using pip:

```
pip install git+https://github.com/yourusername/fb_data.git
```

## Usage

```python
from fb_data import Snowflake

# Initialize Snowflake connection
sf = Snowflake(
    user="your_username",
    password="your_password",
    account='your_account',
    warehouse='your_warehouse',
    database='your_database',
    schema='your_schema',
    role='your_role'
)

# Execute a query
result = sf.execute_query("SELECT * FROM your_table LIMIT 10")

# Execute a query and get results as a DataFrame
df = sf.execute_query_to_dataframe("SELECT * FROM your_table LIMIT 10")

# Write a DataFrame to Snowflake
import pandas as pd
df = pd.DataFrame(...)  # Your data here
sf.write_dataframe_to_table(df, 'your_table', if_exists='replace')

# Close the connection
sf.close()
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.