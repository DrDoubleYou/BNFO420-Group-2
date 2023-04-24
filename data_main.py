import csv
import plotly.express as px
import pandas as pd
import os

#a script that will be ignored by GIT containing countries and their case counts by month
from cases_list import cases_list 

global months, months_d, countries

jan=['Jan']
feb=["Feb"]
mar=["Mar"]
apr=["Apr"]
may=["May"]
jun=["Jun"]
jul=["Jul"]
aug=["Aug"]
sep=["Sep"]
oct=["Oct"]
nov=["Nov"]
dec=["Dec"]

months = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]

months_d={"jan":"1","feb":"2","mar":"3","apr":"4","may":"5","jun":"6","jul":"7","aug":"8",\
          "sep":"9","oct":"10","nov":"11","dec":"12"}

class data():
    def __init__(self, get_all_countries=False,):

        self.c=0
        if get_all_countries == True:
            #run functions to write file of similar countries in misinfo & stringency datasets
            self.all_countries()
            self.stringency_countries()
            self.misinfo_countries()
            self.sim_countries()
        
        else:
            #if data has already been gathered, just put similar contries in list
            with open('all_countries.txt',"r") as f:

                self.both  = list(csv.reader(f))
                for item in self.both[:-1]:
                    self.both[self.both.index(item)]=item[0]

    def all_coutnries(self):

        """
        This function extracts all countries from the countries of the world dataset    
        """

        #generate list of countries of the world
        self.all_countries=[]
        with open('misinfo\\countries.csv',"r") as f:

            reader_obj = csv.reader(f)

            for row in list(reader_obj):
                self.all_countries.append(row[0].strip())

    def stringency_countries(self):

        """
        This function extracts all countries from the stringency dataset    
        """

        self.w_countries=set()
        with open('misinfo\\stringency.csv',"r") as f:

            reader_obj = csv.reader(f)

            for row in list(reader_obj):
                self.w_countries.add(row[2].strip())

    def misinfo_countries(self):

        """
        This function extracts all countries from the misinformation dataset    
        """

        #open and parse through the misinformation database
        self.m_countries=set()
        with open('misinfo\\misinfo.csv',"r",encoding="utf8") as f:

            reader_obj = csv.reader(f)
            
            for row in list(reader_obj):
                print(row[14])
                #seperate cells where multuple countries are listed
                if "," in row[14]:
                    add=row[14].split(",")
                    [self.m_countries.add(c.strip()) for c in add]
                else:
                    self.m_countries.add(row[14].strip())

    def sim_countries(self, print_=False):

        """
        This function determines the countries that are similar between the 
        misinformation dataset, stringency dataset, and all countries of the 
        world dataset
        """

        self.both = []

        #determine which/how many countries are similar
        for country in self.w_countries:
            if ((country in self.w_countries) and (country in self.m_countries) and (country in self.all_countries)):
                self.both.append(country)

        if print_==True:
            print(f"Here is a list of all countries that are in both datasets:{self.both}\n\
                   Legnth of this dataset: {len(self.both)} countries")


        with open(f'datasets\\similar_countries.txt',"w") as f:
            for country in self.both:
                f.write(f"{country}")

    def stringency_data(self, country, year):

        stringency = []

        with open('stringency_updated.csv',"r",encoding="utf8") as f:
            
            reader = list(csv.reader(f))

            for row in reader:
                #if row is the last of a month (where we take out measurement) and for this year is 2020
                try:
                    if ((row[2] == country) and (row[3][:2]!=reader[reader.index(row)+1][3][:2]) and (row[3][-4:]==y)):
                        stringency.append(f"{row[2]}{row[47]}")
                    else:
                        continue
                except:
                    pass
        
        self.stringency_nums=[]
        for item in stringency:
            self.stringency_nums.append(item.replace(country,""))

    def misinfo_data(self, country, year, graph=False):
        """
        This function will  add each misinformation story from each month to its
        corresponding country. Set graph to True when calling to display figure
        """

        with open(f'datasets\\misinfo.csv',"r",encoding="utf8") as f:

            reader_obj = csv.reader(f)

            for row in list(reader_obj):
                if country in row[14]:
                    for month in months:

                        #match the month name
                        if month[0].lower()==row[12][-6:-3].lower():
                            if "," in row[14]:
                                add=row[14].split(",")
                                [month.append(a) for a in add]
                            else:
                                month.append(row[14])
            # Create the visual
            if graph==True:
                df = pd.DataFrame(dict(

                    group = self.both,
                    values = [months[6].count(country) for country in self.both]))

                fig = px.bar(df, x = 'group', y = 'values',
                            title = "Number of Misinformation Stories By Country in June",
                            labels = {'group': 'Country', 'value':'Number of Misinformation Stories'},
                            color = 'group')
                
        self.misinfo_nums=[]
        for month in months:
            self.misinfo_nums.append(str(month.count(country)))

    def ex_mort_data(self, country, year):

        """
        This function will write the data for excess mortality for the given year
        """

        mort=[]
        with open(f'datasets\\excess_mortality.csv',"r",encoding="utf8") as f:
            
            reader = list(csv.reader(f))
            #print(reader

            for row in reader:
                #if row is for a country of interest in 2020
                if ((row[0] in self.both) and (row[0]==country) and (row[2][-4:]==year) and (row[2][:2]!=reader[reader.index(row)+1][2][:2])):
                    mort.append(f"{row[0]}{row[3]}")
        
        if len(mort)==0:
            print(f"{country} is not in this dataset")
            self.c+=1
            self.abort = True
        else:
            self.abort=False

        self.ex_mort_nums=[]

        for item in mort:
            self.ex_mort_nums.append(item.replace(country,""))
            
    def cases_data(self, year, country):

        """
        This function will write the data for total cases by country for the given year
        """
        cases = cases_list(year)

        for item in cases:
            if country in item:
                self.cases = item[1:]

    def master_maker(self,year):
        master=[]
        for file in os.listdir(f"output\\{year}"):
            if file[-3:]=="csv":
                with open(f"output\\{year}\\{file}","r") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if "_" in row[1]:
                            continue
                        else:
                            master.append(row)
            else:
                continue
        with open(f"output\\{year}\\master\\master.csv","w",newline="") as g:
            writer = csv.writer(g)
            writer.writerows(master)

if __name__ == "__main__":
    x = data()
    valid_years = [2020,2021,2022]
    while True:
        #y = input("What year would you like to look at?\n")
        y="2020"
        if int(y) in valid_years:
            break
        else:
            print("Invalid year!")
            continue
    for country in x.both:
        
        output_filepath = f"output\\{y}\\{country[0]}.csv"

        #os.mkdir(f"output_filepath\\{country}.csv")
        x.stringency_data(country=country, year=y)
        #print("Done with STRINGENCY")
        x.misinfo_data(country=country,year=y)
        #print("DONE WITH MISINFO")
        x.ex_mort_data(country=country,year=y)
        #print("DONE WITH EX MORT")
        x.cases_data(country=country,year=y)
        #print("DONE WITH CASES")

        #if first months arent included
        while(len(x.cases)!=12):
            x.cases.insert(0,"")
        while(len(x.ex_mort_nums)!=12):
            x.ex_mort_nums.insert(0,"")
        while(len(x.misinfo_nums)!=12):
            x.misinfo_nums.insert(0,"")
        while(len(x.stringency_nums)!=12):
            x.stringency_nums.insert(0,"")
        print(f"{len(x.stringency_nums)} {len(x.misinfo_nums)} {len(x.ex_mort_nums)} {len(x.cases)}")

        if x.abort==True: #if country not in all_countries
            continue
        else: #write the file in appropriate directory
            df = pd.DataFrame({'misinfo_stories': x.misinfo_nums,
                            'total_cases': x.cases,
                            'excess_mortality': x.ex_mort_nums,
                            'stringency_index': x.stringency_nums})
            df.to_csv(f"output\\{y}\\{country}.csv", index=False)

