import pandas as pd # for csv related functions
import numpy as np # for mathematical use
import matplotlib.pyplot as plt # for data visualisation
import sys # for command line arguments
import os # to create directory
import shutil # for folder deletion
import stat # for folder removal

def rmtree(top):
    for root, dirs, files in os.walk(top, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            try:
                os.chmod(filename, stat.S_IWRITE)
                os.remove(filename)
            except PermissionError:
                print(f"Permission denied: {filename}. Trying to force delete.")
                try:
                    os.remove(filename)
                except Exception as e:
                    print(f"Failed to delete {filename}: {e}")

        for name in dirs:
            dirpath = os.path.join(root, name)
            try:
                os.rmdir(dirpath)
            except OSError as e:
                print(f"Failed to delete {dirpath}: {e}")
                # Try using shutil if os.rmdir fails
                try:
                    shutil.rmtree(dirpath)
                except Exception as e:
                    print(f"shutil failed to delete {dirpath}: {e}")

    try:
        os.rmdir(top)
    except OSError as e:
        print(f"Failed to delete the top directory {top}: {e}")
        try:
            shutil.rmtree(top)
        except Exception as e:
            print(f"shutil failed to delete the top directory {top}: {e}")

# Path to the "stats" folder
folder_path = 'stats'

# Check if the folder exists before attempting to delete
if os.path.exists(os.path.join(folder_path, sys.argv[1])):
    rmtree(folder_path + '/' + sys.argv[1])
    print(f"The folder '{folder_path}//" + sys.argv[1] + "' and all its contents have been deleted.")
else:
    print(f"The folder '{folder_path}/" + sys.argv[1] + "' does not exist.")
    
# Path to the "plots" folder
folder_path = 'plots'

# Check if the folder exists before attempting to delete
if os.path.exists(os.path.join(folder_path, sys.argv[1])):
    rmtree(folder_path + '/' + sys.argv[1])
    print(f"The folder '{folder_path}/" + sys.argv[1] + "' and all its contents have been deleted.")
else:
    print(f"The folder '{folder_path}/" + sys.argv[1] + "' does not exist.")

if not os.path.exists('stats'):
    os.mkdir('stats')
    
if not os.path.exists('plots'):
    os.mkdir('plots')

# make the directory for the year if it does not exist
if not os.path.exists(os.path.join('stats', sys.argv[1])):
    os.mkdir(os.path.join('stats', sys.argv[1]))

if not os.path.exists(os.path.join('plots', sys.argv[1])):
    os.mkdir(os.path.join('plots', sys.argv[1]))

# read the monthly spendings csv, pass the year as a command line argument when running the script
df_spendings = pd.read_csv("data/" + sys.argv[1] + "_monthly_spendings.csv", sep = ",")

print("\nSuccessfully read the monthly spendings CSV for year", sys.argv[1])

# read the monthly earnings csv, pass the year as a command line argument when running the script
df_earnings = pd.read_csv("data/" + sys.argv[1] + "_monthly_earnings.csv", sep = ",")

print("\nSuccessfully read the monthly earnings CSV for year", sys.argv[1])

###########################################################

# retrieve the months
months = df_spendings.Month.unique()

print("\n", months)

# initialize a new dataframe to store monthly stats in it
stats = pd.DataFrame(columns=["Month", "Event", "Amount", "Percentage"])

print("----------------------------")
print("\nWill now save stats for year " + sys.argv[1])

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

if not os.path.exists('stats/' + sys.argv[1] + '/month'):
    os.mkdir('stats/' + sys.argv[1] + '/month')

stats.to_csv("stats/" + sys.argv[1] + "/month/" + sys.argv[1] + "_monthly_stats.csv", index = False)

###########################################################

if not os.path.exists('stats/' + sys.argv[1] + '/events'):
    os.mkdir('stats/' + sys.argv[1] + '/events')
    
if not os.path.exists('plots/' + sys.argv[1] + '/events'):
    os.mkdir('plots/' + sys.argv[1] + '/events')
    
if not os.path.exists('plots/' + sys.argv[1] + '/year'):
    os.mkdir('plots/' + sys.argv[1] + '/year')
    
if not os.path.exists('stats/' + sys.argv[1] + '/year'):
    os.mkdir('stats/' + sys.argv[1] + '/year')
    
if not os.path.exists('plots/' + sys.argv[1] + '/month'):
    os.mkdir('plots/' + sys.argv[1] + '/month')
    
if not os.path.exists('stats/' + sys.argv[1] + '/month'):
    os.mkdir('stats/' + sys.argv[1] + '/month')


print("----------------------------")
print("\nWill now plot line graphs!")

events = stats.Event.unique()

e_yearly = pd.DataFrame(columns = ["Event", "Amount", "Monthly_average"])

# check each event and then each month to see what was spent on that event each month
for e in events:
    # list to store the amount spent for that event for each month
    amounts = []
    for m in months:
        df_month = stats[stats["Month"] == m]
        df_event = df_month[df_month["Event"] == e]
        
        # check whether there was this particular event, get the no. of rows
        no_of_events = df_event.shape[0]
        
        # if there were no events then add 0, else add the amount
        if no_of_events == 0:
            amounts = amounts + [0]
        else:
            amounts = amounts + [df_event.Amount.tolist()[0]]

    # create a dataframe
    e_monthly = pd.DataFrame({"Month": months, "Amount": amounts})
    e_monthly.to_csv("stats/" + sys.argv[1] + "/events/" + sys.argv[1] + "_" + e + "_monthly_spendings.csv", index = False)
    
    e_yearly = e_yearly.append({"Event": e, "Amount": np.round(np.sum(amounts), 2), "Monthly_average": np.round(np.average(amounts), 2)}, ignore_index = True)
            
    plt.figure(figsize=(14, 8))  # Increase width for better spacing
    
    # Plot the first line
    plt.plot(months, amounts, marker='o', linestyle='-', color='b', 
            label='Amount spent EUR ' + str(np.round(np.sum(amounts), 2)))
    
    # Add a title and labels
    plt.title('Amount spent monthly for ' + e + ' for year ' + sys.argv[1])
    plt.xlabel('Month')
    
    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha='right')  
    
    # Add values on points
    for i, txt in enumerate(amounts):
        plt.text(months[i], amounts[i], str(round(txt, 2)), 
                ha='center', va='bottom', fontsize=12, color='black')
    
    # Add a grid
    plt.grid(True)
    
    # Show the legend
    plt.legend()
    
    # Save the figure
    plt.savefig("plots/" + sys.argv[1] + "/events/" + sys.argv[1] + "_" + e + "_monthly_spendings.png")        
    plt.close()
    # plot for each month
    print("\nPlotted amounts spent monthly for " + e)
    print("Total: " + str(np.round(np.sum(amounts), 2)))
    print("Monthly average: " + str(np.round(np.average(amounts), 2)))

###############################################

if not os.path.exists('plots/' + sys.argv[1] + '/month/per_event'):
    os.mkdir('plots/' + sys.argv[1] + '/month/per_event')

if not os.path.exists('stats/' + sys.argv[1] + '/month/per_event'):
    os.mkdir('stats/' + sys.argv[1] + '/month/per_event')


# check each event and then each month to see what was spent on that event each month
for e in events:
    # list to store the amount spent for that event for each month
    month_event_spendings = []
    
    for m in months:
        df_month = stats[stats["Month"] == m]
        df_event = df_month[df_month["Event"] == e]
        
        # check whether there was this particular event, get the no. of rows
        no_of_events = df_event.shape[0]
        
        # if there were no events then add 0, else add the amount
        if no_of_events == 0:
            month_event_spendings.append(0)
        else:
            month_event_spendings.append(np.sum(df_event.Amount.tolist()))

    # create a dataframe
    e_monthly = pd.DataFrame({"Month": months, "Amount": month_event_spendings})
    e_monthly.to_csv("stats/" + sys.argv[1] + "/month/per_event/" + sys.argv[1] + "_" + e + ".csv", index = False)
    
    # Plotting the line graph
    plt.figure(figsize=(10, 6))
    plt.plot(months, month_event_spendings, marker='o', linestyle='-', label=e)

    # Add value labels at each data point
    for i, value in enumerate(month_event_spendings):
        plt.text(months[i], value, str(value), ha='center', va='bottom')

    plt.title(f"Monthly Spending for Event: {e}")
    plt.xlabel("Month")
    plt.ylabel("Amount Spent")
    plt.grid(True)
    plt.tight_layout()
    plt.xticks(rotation=45)  # rotate if months are long
    plt.savefig("plots/" + sys.argv[1] + "/month/per_event/" + sys.argv[1] + "_" + e + ".png")
    plt.close()
    
###############################################


import numpy as np
import matplotlib.pyplot as plt
import sys

# Sort data by Amount in descending order
e_yearly_sorted = e_yearly.sort_values(by="Amount", ascending=False)

index = np.arange(len(e_yearly_sorted))  # Ensure correct indexing

plt.figure(figsize=(20, 10))  # Width = 20, Height = 10

# Create the sorted bar chart
bar_width = 0.6  
bars = plt.bar(index, e_yearly_sorted.Amount.tolist(), width=bar_width, color='royalblue', label='Spending')

# Add text labels **above** the bars
for bar, amount in zip(bars, e_yearly_sorted.Amount.tolist()):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max(e_yearly_sorted.Amount) * 0.02), 
             f'{amount:.2f}', ha='center', va='bottom', fontsize=9, color='black')

# Add labels and title
plt.title('Yearly Event Spendings in EUR', fontsize=16)
plt.xlabel('Event', fontsize=14)
plt.ylabel('Spending in EUR', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(index, e_yearly_sorted.Event.tolist(), rotation=45, ha="right")

plt.tight_layout()  

# Save the plot
plt.savefig(f"plots/{sys.argv[1]}/year/{sys.argv[1]}_event_spendings.png")
plt.close()

# ======== SECOND BAR CHART ======== #

# Sort data by Monthly Average in descending order
e_yearly_sorted = e_yearly.sort_values(by="Monthly_average", ascending=False)

index = np.arange(len(e_yearly_sorted))

plt.figure(figsize=(20, 10))  # Width = 20, Height = 10

# Create the sorted bar chart
bars = plt.bar(index, e_yearly_sorted.Monthly_average.tolist(), width=bar_width, color='royalblue', label='Spending')

# Add text labels **above** the bars
for bar, amount in zip(bars, e_yearly_sorted.Monthly_average.tolist()):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (max(e_yearly_sorted.Monthly_average) * 0.02), 
             f'{amount:.2f}', ha='center', va='bottom', fontsize=9, color='black')

# Add labels and title
plt.title('Monthly Average Event Spendings', fontsize=16)
plt.xlabel('Event', fontsize=14)
plt.ylabel('Monthly Average Spending in EUR', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(index, e_yearly_sorted.Event.tolist(), rotation=45, ha="right")

plt.tight_layout()

# Save the plot
plt.savefig(f"plots/{sys.argv[1]}/year/{sys.argv[1]}_monthly_average_event_spendings.png")
plt.close()

e_yearly.to_csv("stats/" + sys.argv[1] + "/year/" + sys.argv[1] + "_yearly_spendings.csv", index = False)

print("\nSaved and plotted the yearly stats")
    
###########################################################
print("----------------------------")
print("\nWill now plot bar graphs!")

# Iterate over the months
for m in months:
    # Filter data for the specific month
    df_month = stats[stats["Month"] == m]
    
    labels_ = df_month.Event
    amounts = df_month.Amount

    # Sort labels and amounts in descending order based on Amount
    sorted_data = sorted(zip(labels_, amounts), key=lambda x: x[1], reverse=True)
    labels, amounts = zip(*sorted_data)

    # Generate formatted labels for the legend
    legend_labels = [f'{l}, EUR {a:.2f}, {(a / np.sum(amounts)) * 100:.1f}%' for l, a in sorted_data]

    # Create a larger figure
    plt.figure(figsize=(20, 10))

    # Create the bar chart
    bar_width = 0.6
    index = np.arange(len(labels))

    bars = plt.bar(index, amounts, width=bar_width, color='royalblue', label='Spending')

    # Add text labels on top of bars
    for bar, amount in zip(bars, amounts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), 
                 f'{amount:.2f}', ha='center', va='bottom', fontsize=9)

    # Add labels and title
    plt.title("Monthly Spendings for " + m + " " + sys.argv[1], fontsize=20)
    plt.xlabel("Event", fontsize=14)
    plt.ylabel("Spending in EUR", fontsize=14)
    plt.xticks(index, labels, rotation=45, ha="right")  # Rotate labels for readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adjust layout
    plt.tight_layout()

    # Save the bar chart
    plt.savefig(f"plots/{sys.argv[1]}/month/{sys.argv[1]}_{m}_spendings.png")
    plt.close()

    print("\nPlotted for", m)
 
###########################################################
if len(sys.argv) > 2:
    if sys.argv[2] is 'y':

        if not os.path.exists('plots/' + sys.argv[1] + '/sports'):
            os.mkdir('plots/' + sys.argv[1] + '/sports')
            
        if not os.path.exists('stats/' + sys.argv[1] + '/sports'):
            os.mkdir('stats/' + sys.argv[1] + '/sports')
        
        print("----------------------------")
        print("\nWill now count how much money was spent on Sports and how much we attended in " + sys.argv[1])
        
        att = 0
        total = 0
        
        # Create dataframes to store stats in them
        total_sports = pd.DataFrame(columns=["Attended", "Amount", "Average_att_per_month", "Average_spent_per_month"])
        monthly_sports = pd.DataFrame(columns=["Month", "Attended", "Amount"])
        
        # for each month count how many football we attended
        for m in months:
            print("\nRetrieved the data for", m)
            df_month = df_spendings[df_spendings["Month"] == m]
            df_football = df_month[df_month["Event"] == 'Sports']
            if df_football.shape[0] > 0:
                # retrieve the amount of times we attended sports
                a = df_month['Event'].value_counts()['Sports']
                # retrieve the money spent on sports
                t = np.sum(df_football.Amount)
                # add the total number of instances and amount spent
                att += a
                total += t
                # append the data in the stats csv
                monthly_sports = monthly_sports.append({"Month": m, "Attended": a, "Amount": t}, ignore_index = True)
            else:
                print("\nNo sports was played during", m)
                monthly_sports = monthly_sports.append({"Month": m, "Attended": 0, "Amount": 0}, ignore_index = True)
        
        print("\nTotal yearly sports stats:")
        print("EUR " + str(total))
        print("Attended " + str(att))
        print("Average spent per month EUR", str(np.round(total/len(months), 2)))
        print("Average att. per month", str(np.round(att/len(months), 2)))
        
        # append the data in the stats csv
        total_sports = total_sports.append({"Attended": att, "Amount": total, "Average_att_per_month": np.round(att/len(months), 2), "Average_spent_per_month": np.round(total/len(months), 2)}, ignore_index = True)
        
        total_sports.to_csv("stats/" + sys.argv[1] + "/sports/" + sys.argv[1] + "_sports_yearly_stats.csv", index = False)
        monthly_sports.to_csv("stats/" + sys.argv[1] + "/sports/" + sys.argv[1] + "_sports_monthly_stats.csv", index = False)

        print("\nStats saved!")
        
        print("\nWill now plot sports data!")
        
        plt.figure()
        
        # Plot the first line
        plt.plot(months, monthly_sports.Attended, marker='o', linestyle='-', color='b', label='Sports attended ' + str(att))

        # Plot the second line
        plt.plot(months, monthly_sports.Amount, marker='s', linestyle='--', color='r', label='Spent on sports EUR' + str(total))

        # Add a title and labels
        plt.title('Sports stats for year ' + sys.argv[1])
        plt.xlabel('Month')

        # Add a grid
        plt.grid(True)

        # Show the legend
        plt.legend()

        # Display the graph
        plt.savefig("plots/" + sys.argv[1] + "/sports/" + sys.argv[1] + "_sports_stats.png")
        plt.close()
        
        print("\nPlotted sports data!")

###########################################################

print("\nWill now calculate how much we managed to save in " + sys.argv[1])

# Createdataframe storing thje total spend for each month
total_month_spend = pd.DataFrame(columns = ["Month", "Spent"])

# Createdataframe storing thje total saved for each month
total_month_save = pd.DataFrame(columns = ["Month", "Saved"])

# Createdataframe storing thje total saved for each month
total_month_earn = pd.DataFrame(columns = ["Month", "Earned"])

for m in months:
    # get the spendings for the month
    month_spend = stats[stats.Month == m]
    
    # sum the amount spent for the month
    s = np.sum(month_spend.Amount)
    
    # append the monthly spend for the month
    total_month_spend = total_month_spend.append({"Month": m, "Spent": s}, ignore_index = True)
    
    # calculate the earnings for the month
    month_earn = df_earnings[df_earnings.Month == m]
    
    # sum the amount earned for the month
    e = np.sum(month_earn.Net_pay)
    
    # calculate the amount saved
    saved = e - s        
    
    # append the monthly saved for the month
    total_month_save = total_month_save.append({"Month": m, "Saved": saved}, ignore_index = True)
    
    # append the monthly earned for the month
    total_month_earn = total_month_earn.append({"Month": m, "Earned": e}, ignore_index = True)
    
    print("\nCalculated for " + m)

total_month_save.to_csv("stats/" + sys.argv[1] + "/month/" + sys.argv[1] + "_monthly_savings.csv", index = False)
total_month_spend.to_csv("stats/" + sys.argv[1] + "/month/" + sys.argv[1] + "_monthly_spendings.csv", index = False)
total_month_earn.to_csv("stats/" + sys.argv[1] + "/month/" + sys.argv[1] + "_monthly_earnings.csv", index = False)

print("\nSaved the CSVs!")

###########################################################

print("\nWill now plot earnings, spendings and savings for each month in " + sys.argv[1])

# Convert data to lists
saved_values = total_month_save.Saved.tolist()
spend_values = total_month_spend.Spent.tolist()
earn_values = total_month_earn.Earned.tolist()

x = np.arange(len(months))  # the label locations

width = 0.25  # width of the bars

plt.figure(figsize=(12, 6))

# Plot bars for each category
bars1 = plt.bar(x - width, saved_values, width, label='Saved EUR ' + str(np.sum(saved_values)), color='b')
bars2 = plt.bar(x, spend_values, width, label='Spent EUR ' + str(np.sum(spend_values)), color='r')
bars3 = plt.bar(x + width, earn_values, width, label='Earned EUR ' + str(np.sum(earn_values)), color='g')

# Annotate each bar with its value
def annotate_bars(bars, color):
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.0f}', ha='center', va='bottom', fontsize=8, color=color)

annotate_bars(bars1, 'b')
annotate_bars(bars2, 'r')
annotate_bars(bars3, 'g')

# Title and labels
plt.title('Amounts earned, spent and saved monthly for year ' + sys.argv[1])
plt.xlabel('Month')
plt.xticks(x, months)  # set the month labels
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()

# Save and close
plt.tight_layout()
plt.savefig("plots/" + sys.argv[1] + "/month/" + sys.argv[1] + "_monthly_e_s_s_bar.png")        
plt.close()

print("\nSuccessfully plotted the graphs!")
    
print("\nFor year " + sys.argv[1])
print("Earned: " + str(np.sum(total_month_earn.Earned)))
print("Spent: " + str(np.sum(total_month_spend.Spent)))
print("Saved: " + str(np.sum(total_month_save.Saved)))

###########################################################

year = sys.argv[1]
earned = np.sum(total_month_earn.Earned)
spent = np.sum(total_month_spend.Spent)
saved = np.sum(total_month_save.Saved)

# Create a DataFrame
summary_df = pd.DataFrame({
    "Year": [year],
    "Earned": [earned],
    "Spent": [spent],
    "Saved": [saved]
})
            
if not os.path.exists("stats/" + sys.argv[1] + "/summary/"):
            os.mkdir("stats/" + sys.argv[1] + "/summary/")

# Save to CSV
summary_df.to_csv("stats/" + sys.argv[1] + "/summary/" + sys.argv[1] + "_summary.csv", index=False)

print("Summary saved to summary.csv")

###########################################################

print("----------------------------")
print("\nFinished!")