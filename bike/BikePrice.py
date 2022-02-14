# importing the libraries
from statistics import median

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import warnings
warnings.filterwarnings("ignore")

def print_company_names(ds):
    print("\nCase motociclistiche: ");
    for c in ds["CompanyName"].unique():
        print(" - " + c);

# Defining the map function
def dummies(x, df):
    temp = pd.get_dummies(df[x], drop_first=True)
    df = pd.concat([df, temp], axis=1)
    df.drop([x], axis=1, inplace=True)
    return df

ds = pd.read_csv('BikePrices.csv')

# Splitting company name from BikeName column
CompanyName = ds['BikeName'].apply(lambda x: x.split(' ')[0])
ds.insert(3, "CompanyName", CompanyName)
ds.drop(['BikeName'], axis=1, inplace=True)



ds.CompanyName = ds.CompanyName.str.lower()

# Fuel economy
ds['fueleconomy'] = (0.55 * ds['citympg']) + (0.45 * ds['highwaympg'])

# Binning the Bike Companies based on avg prices of each Company.
ds['price'] = ds['price'].astype('int')
temp = ds.copy()
table = temp.groupby(['CompanyName'])['price'].mean()
temp = temp.merge(table.reset_index(), how='left', on='CompanyName')
bins = [0, 10000, 20000, 40000]
ds_bin = ['Budget', 'Medium', 'Highend']
ds['bikerange'] = pd.cut(temp['price_y'], bins, right=False, labels=ds_bin)

ds_lr = ds[['price', 'fueltype', 'aspiration','drivewheel', 'wheelbase',
                'curbweight', 'enginetype', 'cylindernumber', 'enginesize', 'boreratio', 'horsepower',
                'fueleconomy', 'bikelength', 'bikewidth', 'bikerange']]



# Applying the function to the ds_lr
ds_lr = dummies('fueltype', ds_lr)
ds_lr = dummies('aspiration', ds_lr)
ds_lr = dummies('drivewheel', ds_lr)
ds_lr = dummies('enginetype', ds_lr)
ds_lr = dummies('cylindernumber', ds_lr)
ds_lr = dummies('bikerange', ds_lr)

num_vars = ['curbweight', 'enginesize', 'horsepower', 'bikewidth', 'Highend']

Y = ds_lr['price'].values
X = ds_lr[num_vars].values

# train and test split
np.random.seed(0)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, train_size=0.7, test_size=0.3, random_state=100)

# Standardization
ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

def try_model(model, parameters, X_train, Y_train, X_test, Y_test):
    mod = GridSearchCV(model, parameters, cv=None)
    mod.fit(X_train, Y_train)
    return mod

parameters = {'fit_intercept': [True, False], 'normalize': [True, False], 'copy_X': [True, False]}
polyfeats = PolynomialFeatures(degree=2)
X_train_poly = polyfeats.fit_transform(X_train)
X_test_poly = polyfeats.transform(X_test)
mod = try_model(LinearRegression(), parameters, X_train_poly, Y_train, X_test_poly, Y_test)

def valore_nullo(feature, a, min, max):
    if feature == "":
        print("VALORE NON INSERITO --- E' STATO INSERITO VALORE MEDIANA")
        feature = median(a)
    elif float(feature) < min or float(feature) > max:
        print("VALORE NON VALIDO --- E' STATO INSERITO VALORE MEDIANA")
        feature = median(a)
    return feature

# Acquisizione features in input
print("\n-------------  FEATURES PER LA PREDIZIONE DEL PREZZO DELLA MOTO --------------")

print("\nInserire il peso della moto in libbre (VALORI DI RIFERIMENTO MIN:1488 lb, MAX:4066 lb)")
curbweight = valore_nullo(input(), ds_lr["curbweight"].values, 1488, 4066)
print("----------------------------------------------------------------------------------")

print("\nInserire la dimensione del motore in cubic inch (VALORI DI RIFERIMENTO MIN:61 ci, MAX:326 ci)")
enginesize = valore_nullo(input(), ds_lr["enginesize"].values, 61, 326)
print("----------------------------------------------------------------------------------")

print("\nInserire la potenza dei cavalli in kW (VALORI DI RIFERIMENTO MIN:48 kW, MAX:288 kW)")
horsepower = valore_nullo(input(), ds_lr["horsepower"].values, 48, 288)
print("----------------------------------------------------------------------------------")

print("\nInserire la larghezza della moto in inch (VALORI DI RIFERIMENTO MIN:60 i, MAX:72 i)")
bikewidth = valore_nullo(input(), ds_lr["bikewidth"].values, 60, 72)
print("----------------------------------------------------------------------------------")

flag = True
highend = 0
while flag:
    print_company_names(ds)
    print("\nInserire il nome della casa motociclistica (Es. aprilia)")
    companyname = input()
    if companyname.lower() in ds["CompanyName"].values:
        flag = False
    else:
        print("Nome della casa motociclistica non esiste!!!")
        print("----------------------------------------------------------------------------------")

for row in ds[["CompanyName", "bikerange"]].values:

    company = row[0]
    bikerange = str(row[1])

    if companyname == company:
        if (bikerange == "Highend"):
            highend = 1
        else:
            highend = 0
        break

X_user = np.array([curbweight, enginesize, horsepower, bikewidth, highend])
X_user = X_user.reshape(1, -1)
X_user = ss.transform(X_user)
X_user = polyfeats.transform(X_user)
predict = mod.predict(X_user)

if predict < 1000:
    print("----------------------------------------------------------------------------------")
    print("\nImpossibile calcolare prezzo con questi valori di features!!!")
    print("----------------------------------------------------------------------------------")

else:
    print("\n")
    print("+---------------------------------------------------------------------------+")
    print("|                        PREDIZIONE PREZZO MOTO                             |")
    print("+---------------------------------------------------------------------------+")
    print("| PRICE ---> ", round(predict[0], 2))
    print("+---------------------------------------------------------------------------+")