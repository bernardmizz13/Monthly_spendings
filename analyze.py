import pandas as pd # for csv related functions
import numpy as np # for mathematical use
import matplotlib.pyplot as plt # for data visualisation
import sys # for command line arguments



# read the csv, pass the year as a command line argument when running the script
df = pd.read_csv("data/" + sys.argv[1] + "_monthly_spendings.csv", sep = ",")

print("\nSuccessfully read the CSV for year", sys.argv[1])

print("\nCSV file info:")

print(df.info)