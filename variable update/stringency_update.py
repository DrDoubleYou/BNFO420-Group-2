import csv

"""

all_coutnries.txt can be modified to include any country of the user's choice, and 
this script will create a new csv file containing those coutnries' stringency data
"""

with open ("all_countries.txt", "r") as f:
    r = list(csv.reader(f))
    l=[]
    try:
        [l.append(item[0]) for item in r]
    except:
        pass

with open ("datasets\\stringency.csv", "r") as f:
     
    f = list(csv.reader(f))

    all_countries=[]
    for country in l:
        this_country = []
        for row in f:
            if country not in row:
                continue
            else:
                this_country.append(row)
        [all_countries.append(item) for item in this_country]

    with open("stringency_updated.csv", "w",newline="") as f:
        b = csv.writer(f)
        b.writerows(all_countries)
                    

