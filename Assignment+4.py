


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import re
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}




def get_list_of_university_towns():
    data = []
    with open('university_towns.txt') as uniTowns:
        for line in uniTowns:
#             print(line)
            if line.find('[e') >= 0:
                state = line[:line.find('[')]
#                 print('state = ',state)
                continue
            if '(' in line:
                region = line[:line.find('(')-1]
#                 print('region = ',region)
                data.append([state,region])
            else:
#                 print(line)
                data.append([state,line[:-1]])
    
    df = pd.DataFrame(data,columns=['State','RegionName'])
    
    return df





def get_recession_start():
    df_gdp = pd.ExcelFile('gdplev.xls').parse(skiprows=219)[['1999q4', 9926.1]]
    df_gdp.columns = ['YEARQTR','GDP']
    
    prevYearGdp = 0
    recession = 0
    for index, row in df_gdp.iterrows():
        if row['GDP'] < prevYearGdp:
            recession += 1
        else:
            recession = 0
        if recession == 2:
            return df_gdp.iloc[index-2]['YEARQTR']
            break
        prevYearGdp = row['GDP']

get_recession_start()




def get_recession_end():
    df_gdp = pd.ExcelFile('gdplev.xls').parse(skiprows=219)[['1999q4', 9926.1]]
    df_gdp.columns = ['YEARQTR','GDP']
    
    GdpStart = get_recession_start()
    
    prevYearGdp = df_gdp.iloc[1]['GDP']
    recessionEnd = 0

    df_gdp = df_gdp.loc[df_gdp.loc[df_gdp['YEARQTR'] == GdpStart].index[0]:,:]
    df_gdp.reset_index(inplace=True)
    for index,row in df_gdp.iterrows():
        if row['GDP'] > prevYearGdp:
            recessionEnd += 1
        else:
            recessionEnd = 0
        if recessionEnd == 2:
            return df_gdp.iloc[index]['YEARQTR']
            break
        prevYearGdp = row['GDP']       

get_recession_end()




def get_recession_bottom():
    df_gdp = pd.ExcelFile('gdplev.xls').parse(skiprows=219)[['1999q4', 9926.1]]
    df_gdp.columns = ['YEARQTR','GDP']
    
    gdpStart = get_recession_start()
    gdpEnd= get_recession_end()
    
    df_gdp = df_gdp.loc[df_gdp.loc[df_gdp['YEARQTR'] == gdpStart].index[0]:df_gdp.loc[df_gdp['YEARQTR'] == gdpEnd].index[0],:]
    
    minGdp = df_gdp['GDP'].min()
    df_gdp.reset_index(drop=True, inplace=True)
    
    return df_gdp.loc[df_gdp['GDP'] == minGdp]['YEARQTR'][3]

get_recession_bottom()




def convert_housing_data_to_quarters():
    df_housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    df_housing.set_index(['State','RegionName'],inplace=True)

    df_housing.drop(df_housing.columns[0:49], axis=1, inplace=True)
    df_housing.columns = pd.to_datetime(df_housing.columns)
    df_housing = df_housing.resample('Q', axis=1).mean()
    df_housing = df_housing.rename(columns=lambda col: '{}q{}'.format(col.year, col.quarter))

#     print(df_housing.head())

    for state in df_housing.index.levels[0]:
        oldName = state
        newName = states[state]
        df_housing = df_housing.rename(index={oldName:newName})

    
    
    return df_housing
convert_housing_data_to_quarters()




def run_ttest():
    
    df_housing = convert_housing_data_to_quarters()
    df_unitown = get_list_of_university_towns()
    recession_start = get_recession_start()
    quarter_before_recession = df_housing.columns[df_housing.columns.get_loc(recession_start)-1]
#     print(quarter_before_recession)
    recession_bottom = get_recession_bottom()
    df_housing['PriceRatio'] = df_housing.apply(lambda row:(row['2008q3'] - row['2009q2'])/row['2008q3'],axis=1)
    df_housing.drop(df_housing.columns[:-1],axis=1,inplace=True)
    list_of_unitown = df_unitown.RegionName.tolist()
    bool_array = []
    for region in df_housing.index.get_level_values('RegionName'):
        if region in list_of_unitown:
            bool_array.append(True)
        else:
            bool_array.append(False)
    df_uni_pr = df_housing[bool_array].dropna()
    df_notuni_pr = df_housing[[not i for i in bool_array]].dropna()
    p_value = ttest_ind(df_uni_pr['PriceRatio'],df_notuni_pr['PriceRatio']).pvalue

    return (True,p_value,"university town")
run_ttest()

