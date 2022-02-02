import pandas as pd
import os
import matplotlib.pyplot as plt
from itertools import combinations
from collections import Counter

#Merge 12 months of sales data into a single file

#df = pd.read_csv("./Sales_Data/Sales_April_2019.csv")

files = [file for file in os.listdir('./Sales_Data')]
all_months_data = pd.DataFrame()


for file in files:
    df = pd.read_csv("./Sales_Data/"+file)
    all_months_data = pd.concat([all_months_data, df])


#print(all_months_data.head())

all_months_data.to_csv("all_data2.csv", index=False)

all_data2 = pd.read_csv("all_data2.csv")
#print(all_data2.head())


#Clean up the data - Drop rows of NaN

#nan_df = all_data2[all_data2.isna().any(axis = 1)]
#print(nan_df.head())

all_data2 = all_data2.dropna(how='all')
#print(all_data2.head())

#Drop rows that start with 'Or'(in the data)

all_data2 = all_data2[all_data2['Order Date'].str[0:2] != 'Or']

#Augment Data with additional columns

all_data2['Month'] = all_data2['Order Date'].str[0:2]
all_data2['Month'] = all_data2['Month'].astype('int32')

#print(all_data2.head())

#Convert Columns to the correct type
all_data2['Quantity Ordered'] = pd.to_numeric(all_data2['Quantity Ordered'])
all_data2['Price Each'] = pd.to_numeric(all_data2['Price Each'])

#print(all_data2.head())

# Add a Sales Column

all_data2['Sales'] = all_data2['Quantity Ordered'] * all_data2['Price Each']
#print(all_data2.head())


#Best Month for Sales ? How much was earned that month ?
results = all_data2.groupby('Month').sum()

months = range(1,13)

#plt.bar(months, results['Sales'])
#plt.xticks(months)
#plt.ylabel('Sales in USD $')
#plt.xlabel('Month number')
#plt.show()

#Which City had the highest number of Sales ?

#Add new column called 'City' - split
#all_data2['City'] = all_data2['Purchase Address'].str.split(',', expand=True)[1] + all_data2['Purchase Address'].str.split(',')[2].str.split(' ')[1]

#With Apply
def get_city(address):
    return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]

# With "F" string
all_data2['City'] = all_data2['Purchase Address'].apply(lambda x: f"{get_city(x)} ({get_state(x)})")


#Show Highest number of Sales
city_results = all_data2.groupby('City').sum()
#print(city_results.sort_values(by =['Sales'], ascending = False))
#print(all_data2.head())

#Drop Column

#all_data2.drop(columns ='Column', Inplace = True)

#cities = [city for city, df in all_data2.groupby('City')]

#plt.bar(cities, city_results['Sales'])
#plt.xticks(cities, rotation='vertical', size = 8)
#plt.ylabel('Sales in USD $')
#plt.xlabel('City name')

#plt.show()


#What time to display ads so the customers buy the products ?

all_data2['Order Date'] = pd.to_datetime(all_data2['Order Date'])

all_data2['Hour'] = all_data2['Order Date'].dt.hour
all_data2['Minute'] = all_data2['Order Date'].dt.minute

all_data2['Count'] = 1
#all_data2.head()
#print(all_data2.head())

hours = [hour for hour, df in all_data2.groupby(['Hour'])]

#plt.plot(hours, all_data2.groupby(['Hour']).count()['Count'])
#plt.xticks(hours)
#plt.xlabel('Hour')
#plt.ylabel('Number of Orders')
#plt.grid()
#plt.show()


#What products are most often sold together ?

new_df = all_data2[all_data2['Order ID'].duplicated(keep=False)]

new_df['Grouped'] = new_df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
new_df = new_df[['Order ID', 'Grouped']].drop_duplicates()

#print(new_df.head(20))

count = Counter()

for row in new_df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))

#for key, value in count.most_common(10):
    #print(key, value)


#What product sold the most and why do you think it sold the most ?

product_group = all_data2.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']

products = [product for product, df in product_group]

#plt.bar(products, quantity_ordered)
#plt.xticks(products, rotation='vertical', size = 8)
#plt.ylabel('Quanity Ordered')
#plt.xlabel('Product name')

#plt.show()

prices = all_data2.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color = 'g')
ax1.set_ylabel('Price ($)', color = 'b')
ax1.set_xticklabels(products, rotation = 'vertical', size = 8)

plt.show()
