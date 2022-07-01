# %%
'''import libraries'''

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# %%
'''Based on:
https://www.pauldesalvo.com/how-to-calculate-a-net-promoter-score-nps-using-python/'''


'''create demo data'''

df1 = pd.DataFrame(np.random.randint(9,11,size=(1000, 1)), columns=['How likely are you to reccomend the product?']) #promoters
df2 = pd.DataFrame(np.random.randint(7,9,size=(400, 1)), columns=['How likely are you to reccomend the product?']) #passives
df3 = pd.DataFrame(np.random.randint(0,7,size=(100, 1)), columns=['How likely are you to reccomend the product?']) #detractors

df = pd.concat([df1,df2,df3], ignore_index=True)

df['Country Number'] = np.random.randint(1, 6, df.shape[0]) #assiging a random number to assign a country
df['Traveler Type Number'] = np.random.randint(1, 3, df.shape[0]) #assigning a random number to assign a traveler type

#Function to assign a country name
def country_name(x):
    if x['Country Number'] == 1:
        return 'United States'
    elif x['Country Number'] == 2:
        return 'Canada'
    elif x['Country Number'] == 3:
        return 'Mexico'
    elif x['Country Number'] == 4:
        return 'France'
    elif x['Country Number'] == 5:
        return 'Spain'
    else:
        pass

#Function to assign a traveler type
def traveler_type(x):
    if x['Traveler Type Number'] == 1:
        return 'Business'
    elif x['Traveler Type Number'] == 2:
        return 'Leisure'
    else:
        pass

#apply the function to the numbered columns
df['Country'] = df.apply(country_name, axis=1)
df['Traveler Type'] = df.apply(traveler_type, axis=1)

df[['How likely are you to reccomend the product?', 'Country', 'Traveler Type']] #view to remove the random number columns for country and traveler type
# %%
df.head()
# %%
'''Melt the dataframe'''

melted_df = pd.melt(frame = df, id_vars = ['Country','Traveler Type'], value_vars = ['How likely are you to reccomend the product?'],value_name='Score', var_name = 'Question' )

melted_df = melted_df.dropna()

melted_df['Score'] = pd.to_numeric(melted_df['Score'])
melted_df
# %%

'''create categories for the scores'''

def nps_bucket(x):
    if x > 8:
        bucket = 'promoter'
    elif x > 6:
        bucket = 'passive'
    elif x>= 0:
        bucket = 'detractor'
    else:
        bucket = 'no score'
    return bucket

# %%
'''apply the function and create column'''

melted_df['nps_bucket'] = melted_df['Score'].apply(nps_bucket)
melted_df.head()

# %%
'''Calculate the Net Promoter Score grouped '''

grouped_df = melted_df.groupby(['Country','Traveler Type','Question'])['nps_bucket'].apply(lambda x: (x.str.contains('promoter').sum() - x.str.contains('detractor').sum()) / (x.str.contains('promoter').sum() + x.str.contains('passive').sum() + x.str.contains('detractor').sum())).reset_index()

grouped_df_sorted = grouped_df.sort_values(by='nps_bucket', ascending=True)
# %%
grouped_df_sorted.head()
# %%

'''plot the data'''


sns.set_style("whitegrid")
sns.set_context("poster", font_scale = 1)
f, ax = plt.subplots(figsize=(15,7))

sns.barplot(data = grouped_df_sorted, 
            x = 'nps_bucket', 
            y='Country', 
            hue='Traveler Type',
               ax=ax)
ax.set(ylabel='',xlabel='', title = 'NPS Score by Country and Traveler Type')
ax.set_xlim(0,1)
ax.xaxis.set_major_formatter(plt.NullFormatter())
ax.legend()

#data labels
for p in ax.patches:
    ax.annotate("{:.0f}".format(p.get_width()*100),
                (p.get_width(), p.get_y()),
                va='center', 
                xytext=(-35, -18), #offset points so that the are inside the chart
                textcoords='offset points', 
                color = 'white')
    
plt.tight_layout()
plt.savefig('NPS by Country.png')
plt.show()
# %%
