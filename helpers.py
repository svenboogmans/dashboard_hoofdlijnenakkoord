import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

def preprocess_hoofdlijnen_df(df):
    df.columns = df.columns.astype(str)
    return df.melt(id_vars=('Beschrijving', 'Categorie'), var_name='Jaar', value_name='Bedrag')

def combine_small_value_rows_df(df, final_length, jaar):
    combination_size = len(df) - final_length
    combination_rows = df.sort_values('Bedrag', ascending=False).tail(combination_size)
    combination_sum = combination_rows['Bedrag'].sum()
    df_top = df.sort_values('Bedrag', ascending=False).head(final_length - 1)
    df_top.loc[len(df_top.index)] = ['Overig', 'Overig', jaar, combination_sum]
    return df_top

def transform(data, selected_year):
    data['Bedrag'] = [abs(bedrag) for bedrag in data['Bedrag']]
    data = data.loc[(data['Jaar'] == selected_year)]
    return combine_small_value_rows_df(data, 10, selected_year)

def visualize_top10(subheader, pie_title, chapter_data, selected_year):
    st.subheader(subheader)
    df_ready = transform(chapter_data, selected_year)

    fig = px.pie(df_ready, 
                    values = 'Bedrag',
                    names = 'Beschrijving',
                    title = pie_title)
    fig.update_layout(showlegend=False)

    col1, col2 = st.columns(2)
    col1.table(df_ready[['Beschrijving', 'Bedrag']])
    col2.plotly_chart(fig, use_container_width=True)
    st.columns(1)

def lineplot(data, min, max):
    fig, ax = plt.subplots(figsize=(15,10))
    sns.lineplot(x='Jaar', y='Bedrag', hue='Beschrijving', data=data)
    ax.set_ylim([min - abs(max * 0.1), max + abs(max * 0.1)])
    st.pyplot(fig)
