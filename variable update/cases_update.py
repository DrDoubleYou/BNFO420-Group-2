import csv

"""
all_coutnries.txt can be modified to include any country of the user's choice, and 
this script will create a new csv file containing those coutnries' total cases data
"""

with open('all_countries.txt',"r") as f:

    countries  = list(csv.reader(f))
    for item in countries[:-1]:
        countries[countries.index(item)]=item[0]
cases=[]
with open(f'datasets\\cases_by_month.csv',"r",encoding="utf8") as f:
    
    reader = list(csv.reader(f))

    for row in reader:

        #if row is for a country of interest in 2020
        if ((row[2] in countries) and (row[3][-4:]=="2022") and (row[3][:2]!=reader[reader.index(row)+1][3][:2])):
            cases.append(f"{row[2]}{row[4]}")

all_cases=[]
for country in countries:
    this_cunt=[country]
    for item in cases:
        if country in item:
            this_cunt.append(item.replace(country,""))
            
    all_cases.append(this_cunt)
    
