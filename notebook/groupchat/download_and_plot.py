# filename: download_and_plot.py

import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Download the CSV data from the URL
url = "https://raw.githubusercontent.com/uwdata/draco/master/data/cars.csv"
response = requests.get(url)
data = response.text

# Translate the CSV data into a dataframe
df = pd.read_csv(StringIO(data))

# Plot the relationship between 'Weight' and 'Horsepower(HP)'
plt.scatter(df["Weight"], df["Horsepower(HP)"])
plt.xlabel("Weight")
plt.ylabel("Horsepower")

# Add a grid for better readability
plt.grid(True)

# Add a title to the plot
plt.title("Relationship between Weight and Horsepower")

# Save the plot to a file
plt.savefig("weight_vs_horsepower.png")

print("Plot saved as weight_vs_horsepower.png")
