# filename: print_columns.py

import requests
import pandas as pd
from io import StringIO

# Download the CSV data from the URL
url = "https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv"
response = requests.get(url)
data = response.text

# Translate the CSV data into a dataframe
df = pd.read_csv(StringIO(data))

# Print the fields in the dataframe
print("Columns in the dataframe:", df.columns)
