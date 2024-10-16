# SharePoint to DataFrame

A Python library to fetch data from a SharePoint list and return it as a Pandas DataFrame.

## Installation

You can install the package using pip:

```bash
pip install sharepoint_to_df
```

## Usage

Here is a simple example of how to use the library:

```python
import pandas as pd
from sharepoint_to_df import sharepoint_utils

# Define your SharePoint credentials and site
username = 'your_username'
password = 'your_password'
sharepoint_site = 'https://yourtenant.sharepoint.com/sites/yoursite'
list_name = 'Your List Name'

# Fetch the data from the SharePoint list
df = sharepoint_utils.get_list_view_test(username, password, sharepoint_site, list_name)

# Display the DataFrame
print(df.head())
```

### Parameters

- `username` (str): Your SharePoint username.
- `password` (str): Your SharePoint password.
- `sharepoint_site` (str): URL of your SharePoint site.
- `list_name` (str): Name of the SharePoint list.
- `view_name` (str, optional): Name of the SharePoint view. Default is "All Items".

### Requirements

- `pandas`
- `office365-rest-python-client`

You can install the required dependencies using:

```bash
pip install pandas office365-rest-python-client
```
