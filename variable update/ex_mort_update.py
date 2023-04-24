import csv

"""
all_coutnries.txt can be modified to include any country of the user's choice, and 
this script will create a new csv file containing those coutnries' excess mortality data
"""

with open('all_countries.txt',"r") as f:

    countries  = list(csv.reader(f))
    for item in countries[:-1]:
        countries[countries.index(item)]=item[0]

mort=[]

with open('excess_mort\\excess_mortality.csv',"r",encoding="utf8") as f:
    
    reader = list(csv.reader(f))

    for row in reader:

        #if row is for a country of interest in 2020
        if ((row[0] in countries) and (row[2][-4:]=="2020") and (row[2][:2]!=reader[reader.index(row)+1][2][:2])):
            mort.append(f"{row[0]}{row[3]}")

for country in countries:
    with open(f'excess_mort\\{country}_mort_2020.csv',"w") as f:
        for item in mort:
            if country in item:
                f.write(item.replace(country,""))
                f.write("\n")

