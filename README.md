# Monthly spendings analyzer

Repository containg a python script which visualises monthly spendings for eacy year.

To run scirpt open a python envirnoment in your terminal and run:

```
python analyze.py date
```
Instead of date type in the year for which you wish to analyze the monthly spendings, like for example:

```
python analyze.py 2024
```

If you wish to calculate stats for events denoted by _Sports_ run:

```
python analyze.py 2024 y
```
In folder data there is an example CSV file of how the monthly spendings should be saved and prepared for the python script, before running the script rename the CSV file to _monthly_spendings.csv_

The events list should or can be one of your own, meaning that there is no need for any pre-defined list of events, however, make sure that the same name of events are used across all months of the year.
