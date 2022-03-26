"""
title: unemployment
author: Guillermo Trefogli
date: 2/27/2022
"""
# import os
# os.chdir("C:/Users/guill/OneDrive/Documents/Data and Programming II/HW4/hw4")

# counting days
import datetime
start = datetime.datetime(2022, 1, 11)
today_date = datetime.datetime.now()
count_days = start - today_date
print(count_days)

# operations
import random
random.seed(99)
list1 = random.sample(range(1, 10), 3)
print(list1)

list2_double = [x*2 for x in list1]
print(list2_double)

list_odd = [x for x in list1 if x % 2 != 0]
print(list_odd)

random_number = random.choice(list1)
print(random_number)

# strings
def my_function(x):
    assert isinstance(x, str) is True if len(x) >= 15 else print("Your message should have more than 15 words")
    list_strings = x.split('.')
    for i in range(len(list_strings)):
        list_strings[i] = list_strings[i].lower()
        list_strings[i] = list_strings[i].capitalize()
        one_string = '\n'.join(list_strings)
    return one_string

# testing my_function
message_test = "This message cannot be a short one. At least, It should contain 15 words as minimum lenght"
print(my_function(message_test))

# two datasets
import pandas as pd
df_employ = pd.read_csv("employment.csv")
df_force = pd.read_csv("labor force.csv")

df_employ.info()
df_force.info()

# The two dataframes have information for country, msa, year and month, but one provides 
# employment and the other labor force. The type of join will depend on the type of task. 
# In this case, it would be enough to perform a inner join, which means that the merged 
# dataframe keeps the information for the intersection of the two dataframes on mse column:
df_merged = pd.merge(df_employ, df_force, on = "msa")

# "country", "year", and "month" columns are duplicated after the merge. The reason is because 
# they are present in the two dataframes before the joinning. Using outer join to fix it:
df_merged_dup = pd.merge(df_employ, df_force, how = "outer", indicator = True)

# cleaning the data
df_employ.isnull().sum()
df_force.isnull().sum()

df_employ_na = df_employ.dropna()
df_force_na = df_force.dropna()

# Check for NA again:
df_employ_na.isnull().sum()
df_force_na.isnull().sum()

# Merge again:
df_merged_dupna = pd.merge(df_employ_na, df_force_na, how = "outer", indicator = True)
df_merged_dupna = df_merged_dupna.dropna()

df_merged_dupna["unemploy_date"] = pd.to_datetime(df_merged_dupna[['year', 'month']].assign(DAY=1))

# creating unemplopyment rate:
df_merged_dupna["unemploy_date"] = 1 - (df_merged_dupna["Employment"]/df_merged_dupna["Labor Force"])

# fixing Houston:
df_merged_dupna.loc[df_merged_dupna["msa"].str.contains("Houston"), ["Labor Force"]]= 2733348

# calculating the correct rates:
df_merged_dupna["unemploy_date"] = 1 - (df_merged_dupna["Employment"]/df_merged_dupna["Labor Force"])
    
# unemployment rate as %
df_merged_rate = df_merged_dupna.copy()

def format_7(x):
 rounded_number = '{:.2%}'.format(x)
 return rounded_number 

df_merged_rate["rate %"] = df_merged_rate["unemploy_date"].map(format_7)

# average unemployment rates 
mean_rate = df_merged_dupna["unemploy_date"].mean()
list_rate = df_merged_dupna.loc[df_merged_dupna["unemploy_date"] > mean_rate]

# saving
df_merged_dupna.to_csv('data.csv', index = False)


