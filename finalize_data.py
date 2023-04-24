import csv
import os
import math

"""
This script updates exisiting data sheets with 0s where there would otherwise be 
unavailable data, as well as adds the appriate conutry name next to each data point
in the csv 
"""

def getrows():
    with open("output\\2020\\master\\data.csv","r") as f:
            reader = list(csv.reader(f))
            for row in reader:
                for i in range(len(row)):
                    if row[i]=="":
                        row[i]=0

            return list(reader)

def update(x):
    with open("output\\2020\\master\\data.csv","w",newline="") as fi:
    
        writer=csv.writer(fi)
        writer.writerows(x)
            
x = getrows()
update(x)

misinfo_stories = []
cases = []
mort = []
stringency= []

for row in x:
    misinfo_stories.append(row[0])
    cases.append(row[1])
    mort.append(row[2])
    stringency.append(row[3])

params = [misinfo_stories,cases,mort,stringency]
countries=[]
with open("output\\2020\\master\\master_update.csv","r") as d:
    reader = list(csv.reader(d))
    for file in os.listdir("output\\2020"):
        if "csv" in file:
            countries.append(file[:-4])
    for row in reader[1:]:
        try:
            row.append(countries[math.floor(reader.index(row)/(12))])
        except:
            print(row)
    g = reader

with open("output\\2020\\master\\data_update.csv","w",newline="") as f:
    writer = csv.writer(f)
    writer.writerows(g)

