import os
import sys

work_dir = os.getenv("WORK_DIR")

sys.path.append(work_dir)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor



def prepare_data():
    dfs = {}
    for year in range(2015,2020):
        df = pd.read_csv(f"./data/{year}.csv")
        dfs[year] = df


    dfs[2015].drop(columns=['Standard Error'], inplace=True)

    dfs[2016].drop(columns=['Upper Confidence Interval', 'Lower Confidence Interval'], inplace=True)

    dfs[2017].drop(columns=['Whisker.high', 'Whisker.low'], inplace=True)


    country_region_dict = dict(zip(dfs[2015]['Country'], dfs[2015]['Region']))

    dfs[2017]['Region'] = dfs[2017]['Country'].map(country_region_dict)
    dfs[2018]['Region'] = dfs[2018]['Country or region'].map(country_region_dict)
    dfs[2019]['Region'] = dfs[2019]['Country or region'].map(country_region_dict)

    dfs[2015].drop(columns=['Happiness Rank'], inplace=True)
    dfs[2016].drop(columns=['Happiness Rank'], inplace=True)
    dfs[2017].drop(columns=['Happiness.Rank'], inplace=True)
    dfs[2018].drop(columns=['Overall rank'], inplace=True)
    dfs[2019].drop(columns=['Overall rank'], inplace=True)

    dfs[2017].rename(columns={
        'Happiness.Score': 'Happiness Score',
        'Economy..GDP.per.Capita.': 'Economy (GDP per Capita)',
        'Health..Life.Expectancy.': 'Health (Life Expectancy)',
        'Trust..Government.Corruption.': 'Trust (Government Corruption)',
        'Dystopia.Residual': 'Dystopia Residual'
    }, inplace=True)


    dfs[2018].rename(columns={
        'Country or region': 'Country',
        'Score': 'Happiness Score',
        'GDP per capita': 'Economy (GDP per Capita)',
        'Social support': 'Family',
        'Healthy life expectancy': 'Health (Life Expectancy)',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Trust (Government Corruption)'
    }, inplace=True)

    dfs[2019].rename(columns={
        'Country or region': 'Country',
        'Score': 'Happiness Score',
        'GDP per capita': 'Economy (GDP per Capita)',
        'Social support': 'Family',
        'Healthy life expectancy': 'Health (Life Expectancy)',
        'Freedom to make life choices': 'Freedom',
        'Perceptions of corruption': 'Trust (Government Corruption)'
    }, inplace=True)


    years = [2015, 2016, 2017, 2018, 2019]


    dfs_combined = []

    for year in years:
    
        df_with_year = dfs[year].copy()  
        df_with_year['year'] = year  
        dfs_combined.append(df_with_year)  


    df = pd.concat(dfs_combined, ignore_index=True) 

    region_mapping = {
    'Taiwan Province of China': 'Eastern Asia',
    'Belize': 'Latin America and Caribbean',
    'Hong Kong S.A.R., China': 'Eastern Asia',
    'Somalia': 'Sub-Saharan Africa',
    'Namibia': 'Sub-Saharan Africa',
    'South Sudan': 'Sub-Saharan Africa',
    'United Arab Emirates': 'Middle East and Northern Africa',
    'Trinidad & Tobago': 'Latin America and Caribbean',
    'Northern Cyprus': 'Eastern Europe',
    'North Macedonia': 'Central and Eastern Europe',
    'Gambia': 'Sub-Saharan Africa'
    }

    df['Region'] = df['Region'].fillna(df['Country'].map(region_mapping))

    normalization_regions = {
        'Western Europe': 'West_Europe',
        'North America': 'America',
        'Australia and New Zealand': 'Oceania',
        'Middle East and Northern Africa': 'North_Africa',
        'Latin America and Caribbean': 'America',
        'Southeastern Asia': 'Asia',
        'Central and Eastern Europe': 'East_Europe',
        'Eastern Asia': 'Asia',
        'Sub-Saharan Africa': 'South_Africa',
        'Southern Asia': 'Asia',
        'Eastern Europe': 'East_Europe'
    }


    # Normalize the regions using the mapping
    df['Region'] = df['Region'].map(normalization_regions)

    df.rename(columns={
        'Happiness Score': 'Score',
        'Economy (GDP per Capita)': 'Economy',
        'Health (Life Expectancy)': 'Health',
        'Trust (Government Corruption)': 'Trust',
        'Dystopia Residual' : 'Dystopia'
    }, inplace=True)


    df = pd.get_dummies(df, columns=['Region'], drop_first=True, dtype=int)
    df.drop(columns="Country", inplace=True)

    complete_data = df.dropna(subset=['Dystopia'])
    incomplete_data = df[df['Dystopia'].isna()]

    predictors = [
        'Economy', 
        'Family', 
        'Health', 
        'Freedom', 
        'Trust', 
        'Generosity', 
        'year', 
        'Region_Asia', 
        'Region_East_Europe', 
        'Region_North_Africa', 
        'Region_Oceania',
        'Region_South_Africa',
        'Region_West_Europe'
    ]

    X_train = complete_data[predictors]
    y_train = complete_data['Dystopia']

    model = KNeighborsRegressor(
        n_neighbors=4,  
        leaf_size=12,
        weights='distance'                 
    )
    model.fit(X_train, y_train)

    X_missing = incomplete_data[predictors]
    predicted_values = model.predict(X_missing)

    df.loc[df['Dystopia'].isna(), 'Dystopia'] = predicted_values




    X = df.drop(['Score'], axis=1)
    y = df['Score']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2)

    return X_test, y_test

