from helpers import preprocess_hoofdlijnen_df, visualize_top10, lineplot
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

# Set global variables.
chapters = [
    'A. Structurele lastenverlichting en investeringen',
    'B. Structurele verlaging van uitgaven',
    'C. Structurele lastenverzwaringen (inkomsten)',
    'D. Meerjarige investeringsagenda voor wonen, mobiliteit, landbouw en kerncentrales'
]

years = [
    '2025',
    '2026',
    '2027',
    '2028',
    'Struc.'
]

# Preprocess the data.
dfs_hoofdlijnen_fin = pd.read_excel("hoofdlijnen_fin.ods", sheet_name=None, engine="odf")
dfs_hoofdlijnen_agg = pd.read_excel("hoofdlijnen_agg.ods", sheet_name=None, engine="odf")

for key in dfs_hoofdlijnen_fin.keys():
    dfs_hoofdlijnen_fin[key] = preprocess_hoofdlijnen_df(dfs_hoofdlijnen_fin[key])


# Set global streamlit.
st.set_page_config(layout="wide")
st.title('Dashboard Hoofdlijnenakkoord 2024')
tab1, tab2 , tab3 = st.tabs(['Top 10 maatregelen', 'Ontwikkeling over de tijd', 'Ruwe data'])


# Tab 1: top 10 maatregelen.
with tab1:
    st.header('Top 10 maatregelen')
    selected_year = tab1.selectbox('Jaar:', years)

    visualize_top10('Uitgaven',
                    chapters[0],
                    dfs_hoofdlijnen_fin[chapters[0]],
                    selected_year)

    visualize_top10('Bezuinigingen',
                    chapters[1],
                    dfs_hoofdlijnen_fin[chapters[1]],
                    selected_year)

    visualize_top10('Lastenverzwaringen',
                    chapters[2],
                    dfs_hoofdlijnen_fin[chapters[2]],
                    selected_year)

    data_chapter3 = dfs_hoofdlijnen_fin[chapters[3]]
    data_chapter3 = data_chapter3.loc[(data_chapter3['Categorie'] == 'Investering')]
    visualize_top10('Investeringen uit (groei)fondsen',
                    chapters[3],
                    data_chapter3,
                    selected_year)


# Tab 2: ontwikkeling over de tijd.
with tab2:
    st.header('Ontwikkeling over de tijd')

    st.subheader('Effect van de maatregelen over tijd')

    df_ABC = dfs_hoofdlijnen_agg['agg_ABC']
    df_ABC['Bedrag'] = [abs(bedrag) for bedrag in df_ABC['Bedrag']]
    lineplot(df_ABC, df_ABC['Bedrag'].min(), df_ABC['Bedrag'].max())

    st.subheader('Effect van de investeringen uit (groei)fondsen over tijd. Negatieve waarden duiden op een bezuiniging.')

    df_D = dfs_hoofdlijnen_agg['agg_D']
    lineplot(df_D, df_D['Bedrag'].min(), df_D['Bedrag'].max())

    st.subheader('Ontwikkeling per maatregel')

    selected_chapter = tab2.selectbox('Hoofdstuk:', chapters)
    df = dfs_hoofdlijnen_fin[selected_chapter]
    categories = df['Categorie'].unique()
    beschrijvingen = df['Beschrijving'].unique()
    if categories.size > 1:
        selected_category = tab2.multiselect('Categorieën:', df['Categorie'].unique())
        if selected_category:
            beschrijvingen = df.Beschrijving.loc[df['Categorie'].isin(selected_category)].unique()
        else:
            beschrijvingen = df['Beschrijving'].unique()
    selected_measures = tab2.multiselect('Maatregelen:', beschrijvingen)

    if selected_measures:

        df_selection = df.loc[df['Beschrijving'].isin(selected_measures)]
        lineplot(df_selection, df_selection['Bedrag'].min(), df_selection['Bedrag'].max())

# Tab 3: raw data.
with tab3:
    st.header('Ruwe data')

    for chapter in chapters:
        st.subheader(chapter)
        st.table(dfs_hoofdlijnen_fin[chapter])