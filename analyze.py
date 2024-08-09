import pandas as pd # for csv related functions
import numpy as np # for mathematical use
import matplotlib.pyplot as plt # for data visualisation
import sys # for command line arguments

# read the monthly spendings csv, pass the year as a command line argument when running the script
df_spendings = pd.read_csv("data/" + sys.argv[1] + "_monthly_spendings.csv", sep = ",")

print("\nSuccessfully read the monthly spendings CSV for year", sys.argv[1])

print("\nCSV file info:")

print(df_spendings.info)

# read the monthly earnings csv, pass the year as a command line argument when running the script
df_earnings = pd.read_csv("data/" + sys.argv[1] + "_monthly_earnings.csv", sep = ",")

print("\nSuccessfully read the monthly earnings CSV for year", sys.argv[1])

print("\nCSV file info:")

print(df_earnings.info)

# retrieve the months
months = df_spendings.Month.unique()

print("\n", months)

# initialize a new dataframe to store monthly stats in it
df = pd.new_("")

# iterate the data using the month
for m in months:
    df_month = df_spendings[df_spendings["Month"] == m]
    print("Retrieved the data for", m)
    # retrieve the event type
    events = df_month.Event.unique()
    # iterate the data using the event
    for e in events:
        df_month_event = df_month[df_month["Event"] == e]
        
    print(df)