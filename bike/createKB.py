import numpy as np
import pandas as pd

KNOWLEDGE_BASE_PATH = "../bike/knowledgeBase.pl"

ds = pd.read_csv('BikePrices.csv')

# Splitting company name from BikeName column
CompanyName = ds['BikeName'].apply(lambda x: x.split(' ')[0])
ds.insert(3, "CompanyName", CompanyName)
ds.CompanyName = ds.CompanyName.str.lower()
ds['BikeName'] = ds['BikeName'].apply(lambda x: ' '.join(x.split(' ')[1:]))

file_data = ":- discontiguous companyModel/2.\n\n"
ds.rename({'CompanyName': 'companyName'}, axis=1, inplace=True)
ds.rename({'BikeName': 'bikeName'}, axis=1, inplace=True)

ds['price'] = ds['price'].astype('int')
temp = ds.copy()
table = temp.groupby(['companyName'])['price'].mean()
temp = temp.merge(table.reset_index(), how='left', on='companyName')
bins = [0, 10000, 20000, 40000]
ds_bin = ['budget', 'medium', 'highend']
ds['bikerange'] = pd.cut(temp['price_y'], bins, right=False, labels=ds_bin)

def is_not_blank(s):
    if s and s.strip():
        return True
    return False

# Generating company
for string in np.unique(ds['companyName']):
    if is_not_blank(string):
        file_data += "company(\"" + string + "\").\n"

file_data += "\n"

# Generating fuelType
for string in np.unique(ds['fueltype']):
    if is_not_blank(string):
        file_data += "fuelType(\"" + string + "\").\n"

file_data += "\n"

# Generating model - fuelType
for row in ds.itertuples():
    model = row[3]
    fuel = row[5]
    string = "fuelBike(\"" + model + "\",\"" + fuel + "\")."

    if is_not_blank(model) and is_not_blank(fuel) and (string not in file_data):
        file_data += string + "\n"

file_data += "\n"

# Generating company - model
for row in ds.itertuples():
    company = row[4]
    model = row[3]
    string = "companyModel(\"" + company + "\",\"" + model + "\")."

    if is_not_blank(company) and is_not_blank(model) and (string not in file_data):
        file_data += string + "\n"

file_data += "\n"


# Generating model - bikerange
for row in ds.itertuples():
    company = row[4]
    bikerange = row[23]
    string = "bikerange(\"" + company + "\",\"" + str(bikerange) + "\")."

    if is_not_blank(company) and (string not in file_data):
        file_data += string + "\n"

knowledge_base = open(KNOWLEDGE_BASE_PATH, mode="w")
knowledge_base.write(file_data)
knowledge_base.close()

print("\nFile created in: ", KNOWLEDGE_BASE_PATH)

