import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 Import the data from medical_examination.csv and assign it to the df variable
df = pd.read_csv('medical_examination.csv')

# 2 Create the overweight column in the df variable
df['overweight'] = 0
df.loc[df['weight'] / (df['height'] * df['height'] / 10000) > 25, 'overweight'] = 1

#print(df)

# 3 Normalize data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, set the value to 0. If the value is more than 1, set the value to 1.
df.loc[df['cholesterol']  == 1, 'cholesterol'] = 0
df.loc[df['cholesterol']  > 1, 'cholesterol'] = 1
df.loc[df['gluc']  == 1, 'gluc'] = 0
df.loc[df['gluc']  > 1, 'gluc'] = 1

#print(df)

# 4 Draw the Categorical Plot in the draw_cat_plot function
def draw_cat_plot():
    # 5 Create a DataFrame for the cat plot using pd.melt with values from cholesterol, gluc, smoke, alco, active, and overweight in the df_cat variable.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    #print(df_cat)

    # 6 Group and reformat the data in df_cat to split it by cardio. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    #df_cat = None
    tmp_cat = df_cat.value_counts().reset_index(name='total')
    #print(tmp_cat)

    # 7 Convert the data into long format and create a chart that shows the value counts of the categorical features using the following method provided by the seaborn library import : sns.catplot()

    # 8 Get the figure for the output and store it in the fig variable
    fig = sns.catplot(data=tmp_cat, x='variable', y='total', hue='value', col='cardio', kind='bar', order=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']).figure

    # 9 Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# 10 Draw the Heat Map in the draw_heat_map function
def draw_heat_map():
    # 11 Clean the data in the df_heat variable by filtering out the following patient segments that represent incorrect data:
        # height is less than the 2.5th percentile (Keep the correct data with (df['height'] >= df['height'].quantile(0.025)))
        # height is more than the 97.5th percentile
        # weight is less than the 2.5th percentile
        # weight is more than the 97.5th percentile
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(q=0.025)) & (df['height'] <= df['height'].quantile(q=0.975)) & (df['weight'] >= df['weight'].quantile(q=0.025)) & (df['weight'] <= df['weight'].quantile(q=0.975))]
    #print(df_heat)

    # 12 Calculate the correlation matrix and store it in the corr variable
    corr = df_heat.corr()
    #print(corr)

    # 13 Generate a mask for the upper triangle and store it in the mask variable
    mask = corr.copy()
    for row in range(len(mask)):
        for col in range(len(mask.columns)):
            if (col >= row):
                mask.iloc[row, col] = True
            else:
                mask.iloc[row, col] = False
    #print(mask)

    # 14 Set up the matplotlib figure
    fig, ax = plt.subplots(1)
    
    # 15 Plot the correlation matrix using the method provided by the seaborn library import: sns.heatmap()
    sns.heatmap(corr, annot=True, fmt='.1f', linewidth=.5, mask=mask, vmin=-0.08, vmax=0.24, square=True, center=0)

    # 16 Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
