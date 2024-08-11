import pandas as pd # for csv related functions
import numpy as np # for mathematical use
import matplotlib.pyplot as plt # for data visualisation
import sys # for command line arguments
import os # to create directory

# read the monthly spendings csv, pass the year as a command line argument when running the script
df_spendings = pd.read_csv("data/" + sys.argv[1] + "_monthly_spendings.csv", sep = ",")

print("\nSuccessfully read the monthly spendings CSV for year", sys.argv[1])

#print(df_spendings.info)

# read the monthly earnings csv, pass the year as a command line argument when running the script
df_earnings = pd.read_csv("data/" + sys.argv[1] + "_monthly_earnings.csv", sep = ",")

print("\nSuccessfully read the monthly earnings CSV for year", sys.argv[1])

#print(df_earnings.info)

# retrieve the months
months = df_spendings.Month.unique()

print("\n", months)

# initialize a new dataframe to store monthly stats in it
stats = pd.DataFrame(columns=["Month", "Event", "Amount", "Percentage"])

print("----------------------------")

# iterate the data using the month
for m in months:
    df_month = df_spendings[df_spendings["Month"] == m]
    print("\nRetrieved the data for", m)
    # retrieve the event type
    events = df_month.Event.unique()
    #retrieve the total amount of spendings for that particular month
    spendings = np.sum(df_month.Amount)
    # iterate the data using the event
    for e in events:
        # retrieve certain events during that month
        df_month_event = df_month[df_month["Event"] == e]
        # sum the total amount spent for that particlar event
        sum = np.round(np.sum(df_month_event.Amount), 2)
        # calculate the percentage
        percentage = np.round((sum/spendings) * 100, 2)
        
        # append the data in the stats csv
        stats = stats.append({"Month": m, "Event": e, "Amount": sum, "Percentage": percentage}, ignore_index = True)
        
    print("\nCompleted stats for", m)

stats.to_csv("stats/" + sys.argv[1] + ".csv", index = False)
print("----------------------------")
print("\nWill now plot pie charts!")

if not os.path.exists('plots/' + sys.argv[1]):
    os.mkdir('plots/' + sys.argv[1])

# iterate the stats using the month
for m in months:
    # group the stats by month
    df_month = stats[stats["Month"] == m]
    labels_ = df_month.Event
    amounts = df_month.Amount
    labels = [f'{l}, EUR {s:0.2f}' for l, s in zip(labels_, amounts)]
    # Create a larger figure
    plt.figure(figsize=(19, 19))
    # Plot the pie chart
    pie = plt.pie(amounts,autopct='%1.1f%%', radius=3000, frame=False,   pctdistance=0.85, labeldistance=2.1, startangle=140)
    plt.axis('equal')
    # Add a legend
    plt.legend(bbox_to_anchor=(0.85, 1), loc='upper left', labels=labels, fontsize=15)
    # Add a title
    plt.title("Monthly spendings for " + m + " " + sys.argv[1], fontsize=25)
    # Save the pie chart
    plt.savefig("plots/2024/" + m + "_spendings.png")
    print("\nPlotted for", m)
    
print("----------------------------")
print("Finished!")