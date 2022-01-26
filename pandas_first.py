import pandas as pd
import re

#Load in the data
df = pd.read_csv('pokemon_data.csv')
#or read_excel if its an xlsx file
# or read_csv('filename.txt, delimiter='\t') if it's a txt file

# get the top 3 rows
(df.head(3))
# get the bottom 3 rows
(df.tail(3))

#Read Header
(df.columns)

#Read each column
(df[['Name', 'Type 1', 'HP']])

#Read each row df.head(3) or 
(df.iloc[1:4]) #iloc - integer location

#Read a specific location
(df.iloc[2,1])

#Iterate through rows
#for index,row in df.iterrows():
    #print(index,row)

#Find specific data based on text/num info
(df.loc[df['Type 1'] == "Fire"])

#Describe
(df.describe())

#Sort
(df.sort_values('Name', ascending=False))

(df.sort_values(['Type 1', 'HP'], ascending=[1,0]))

#Add new column
df['Total'] = df['HP'] + df['Attack'] + df['Defense'] + df['Sp. Atk'] + df['Sp. Def'] + df['Speed']
(df.head(5))

#Drop column
df = df.drop(columns=['Total'])
(df.head(5))

#Add new column #2  axis=1 is horizontal, axis=0 is vertical
df['Total'] = df.iloc[:, 4:10].sum(axis=1)
(df.head(5))

#Rearrange columns - using actual column names is probably better
cols = list(df.columns.values)
df = df[cols[0:4] + [cols[-1]] + cols[4:12]]
(df.describe)

#Save data in different formats
#df.to_csv('modified.csv', index = False)
#df.to_excel('modified.xlsx', index = False)
#df.to_csv('modified.txt', index = False, sep='\t')

#Advanced Filtering (& = and, | = or)
new_df = df.loc[(df['Type 1'] == 'Grass') & (df['Type 2'] == 'Poison') & (df['HP'] > 70)]
(new_df)

#Save this data as a new csv
new_df.to_csv('filtered.csv')

#Reset Index in the new dataframe and get rid of the old index
#inplace = True so we dont need "new_df =" at the start
#inplace modifies the original data
new_df.reset_index(drop=True, inplace=True)
new_df.to_csv('filtered.csv')
(new_df)

#Filter out names that contain Mega (~)
(df.loc[~df['Name'].str.contains('Mega')])

#Filter with Regex for 2 conditions
(df.loc[df['Type 1'].str.contains('Fire|Grass', regex = True)])

#Same but ignore case
(df.loc[df['Type 1'].str.contains('fire|grass', flags=re.I, regex = True)])

#Filter - Show only those that start with "pi"
(df.loc[df['Name'].str.contains('^pi[a-z]*', flags=re.I, regex = True)])

#Change the dataframe based on the conditions
df.loc[df['Type 1'] == 'Fire', 'Type 1'] = 'Flamer'
(df)

#Conditions and the edited column can be different
df.loc[df['Type 1'] == 'Flamer', 'Legendary'] = False
(df)

#Reload Dataframe (get rid of previous changes)
df = pd.read_csv('modified.csv')
(df)

#Modify more columns at the same time
df.loc[df['Total'] > 500, ['Generation','Legendary']] = ['Test 1', 'Test 2']
(df)

#Reload Dataframe (get rid of previous changes)
df = pd.read_csv('modified.csv')
(df)

#Aggregate Stats
(df.groupby(['Type 1']).mean().sort_values('Attack', ascending=False))

#sum, count
(df.groupby(['Type 1']).count())

#Put a new column
df['count'] = 1
(df)

#Group by multiple parameters
(df.groupby(['Type 1', 'Type 2']).count()['count'])

#Loading in a smaller size of the data
"""
for df in pd.read_csv('modified.csv', chunksize=5):
    print('CHUNK DF')
    print(df)
"""
#Create new empty Dataframe with the same columns 
new_df = pd.Dataframe(columns=df.columns)

#Building up the new Dataframe chunk by chunk
for df in pd.read_csv('modified.csv', chunksize=5):
    results = df.groupby(['Type 1']).count()

    new_df = pd.concat([new_df, results])
