import streamlit as st
import pandas as pd
import numpy as np


df = pd.read_csv('food_info.csv',index_col='index')
#by city
city = st.selectbox('Select City',['Edinburgh','Glasgow'])
if city == 'Edinburgh':
    df_city = df[df['Restaurant'].str.startswith('EH')]
elif city == 'Glasgow':
    df_city = df[df['Restaurant'].str.startswith('G')]
#by meal
meal = st.selectbox('Select Meal', df_city['Meal Type'].unique())
df_city_meal = df_city[df_city['Meal Type'] == meal]

df_city_meal.loc[:,'Calories Rating'] = df_city_meal.apply(lambda x: 0 if x['Total Calories'] < df_city_meal['Total Calories'].quantile(0.25) else 1 if x['Total Calories'] < df_city_meal['Total Calories'].quantile(0.75) else 2,axis=1)
df_city_meal.loc[:,'Price Adjusted Satisfaction'] = [df_city_meal.loc[:,'Satisfaction Index'].values[x]/df_city_meal.loc[:,'price'].values[x] for x in range(df_city_meal.shape[0])]
df_city_meal = df_city_meal.sort_values(by=['Calories Rating','Price Adjusted Satisfaction'],ascending=[True,False])
df_city_meal.loc[:,'Calories Rating'] = df_city_meal.apply(lambda x: "Low" if x['Total Calories'] < df_city_meal['Total Calories'].quantile(0.25) else "Medium" if x['Total Calories'] < df_city_meal['Total Calories'].quantile(0.75) else "High",axis=1)
df_city_meal = df_city_meal.drop(columns=['Protein','Fibre','Starch','Calories per 100','total weight','Meal Type'])
# st.dataframe(df_city_meal)

df_city_agg = df_city.groupby('Meal Type')['Total Calories'].agg([('mean', np.mean)])
print(df_city_agg)
