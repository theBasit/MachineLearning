

import pandas as pd
import numpy as np
import re 
from functools import reduce





def one():
    energy = pd.read_excel('Energy Indicators.xls',
                             skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                             skipfooter=38,
                             na_values="...",
                             header=None,
                             parse_cols="C:F",
                             names=['Country',
                                    'Energy Supply', 
                                    'Energy Supply per Capita', 
                                    '% Renewable'])

    #  replace the numerics and brackets from country name and convert giga to petajoules
    for index,row in energy.iterrows():
        if row['Country'].find('(') > 0:
            energy = energy.replace(row['Country'],row['Country'][:row['Country'].find('(') - 1])
        regex = re.compile(r'([A-Za-z ,]+)[0-9]')
        if re.findall(regex,row['Country']):
            energy = energy.replace(row['Country'],re.findall(regex,row['Country'])[0])

    energy['Energy Supply'] = energy['Energy Supply'] * 1000000

    #   replace the specific country names with the correct ones 
    energy = energy.replace({"Republic of Korea": "South Korea",
                                "United States of America": "United States",
                                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                "China, Hong Kong Special Administrative Region": "Hong Kong"})

    # # Load the GDP datafram from the specified csv with the required columns
    GDP = pd.read_csv('world_bank.csv',skiprows=4)
    GDP = GDP[['Country Name','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    GDP = GDP.rename(columns={'Country Name':'Country'})
    # Replace the name of specified countries
    GDP = GDP.replace({"Korea, Rep.": "South Korea", 
                            "Iran, Islamic Rep.": "Iran",
                            "Hong Kong SAR, China": "Hong Kong"})


    # # Load the top 15 ScimEn dataframe from the excel file
    ScimEnLong = pd.read_excel('scimagojr-3.xlsx')
    ScimEn = ScimEnLong[:15]

    # # merge all the dataframes into one
    dfList = [ScimEn,energy,GDP]
    
    df = reduce(lambda left,right: pd.merge(left,right,on='Country'),dfList)
    df.set_index('Country',inplace=True)

    # Print the complete dataframe
    #     with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #         print(df.index.size)
    return df




get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')




def two():
    energy = pd.read_excel('Energy Indicators.xls',
                             skiprows=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17],
                             skipfooter=38,
                             na_values="...",
                             header=None,
                             parse_cols="C:F",
                             names=['Country',
                                    'Energy Supply', 
                                    'Energy Supply per Capita', 
                                    '% Renewable'])

    #  replace the numerics and brackets from country name and convert giga to petajoules
    for index,row in energy.iterrows():
        if row['Country'].find('(') > 0:
            energy = energy.replace(row['Country'],row['Country'][:row['Country'].find('(') - 1])
        regex = re.compile(r'([A-Za-z ,]+)[0-9]')
        if re.findall(regex,row['Country']):
            energy = energy.replace(row['Country'],re.findall(regex,row['Country'])[0])

    energy['Energy Supply'] = energy['Energy Supply'] * 1000000

    #   replace the specific country names with the correct ones 
    energy = energy.replace({"Republic of Korea": "South Korea",
                                "United States of America": "United States",
                                "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                                "China, Hong Kong Special Administrative Region": "Hong Kong"})

    # # Load the GDP datafram from the specified csv with the required columns
    GDP = pd.read_csv('world_bank.csv',skiprows=4)
    GDP = GDP[['Country Name','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]
    GDP = GDP.rename(columns={'Country Name':'Country'})
    # Replace the name of specified countries
    GDP = GDP.replace({"Korea, Rep.": "South Korea", 
                            "Iran, Islamic Rep.": "Iran",
                            "Hong Kong SAR, China": "Hong Kong"})


    # # Load the top 15 ScimEn dataframe from the excel file
    ScimEnLong = pd.read_excel('scimagojr-3.xlsx')
    ScimEn = ScimEnLong[:15]

    # # merge all the dataframes into one
    dfList = [ScimEn,energy,GDP]
    
    df = reduce(lambda left,right: pd.merge(left,right,on='Country'),dfList)
    df.set_index('Country',inplace=True)

    # Print the complete dataframe
    #     with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #         print(df.index.size)

    dfList2 = [ScimEnLong,energy,GDP]
    dfUnion = reduce(lambda left,right: pd.merge(left,right,on='Country',how='outer'),dfList2)
    dfIntersection = reduce(lambda left,right: pd.merge(left,right,on='Country',how='inner'),dfList2)
    answer = (len(dfUnion) - len(dfIntersection))
    return answer





def three():
    Top15 = one()
    avgGDP = Top15[['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']].mean(axis=1)
    avgGDP = avgGDP.sort_values(ascending=False)
    return avgGDP




def four():
    Top15 = one()
    avgGDP = three()
    diff = Top15.loc[avgGDP.index[5]]['2015'] - Top15.loc[avgGDP.index[5]]['2006']
    return diff





def five():
    Top15 = one()
    meanESC = Top15['Energy Supply per Capita'].mean()
    return meanESC





def six():
    Top15 = one()
    answer = Top15['% Renewable'].max()
    answer = (Top15[Top15['% Renewable'] == answer].index[0],answer)
    return answer


def seven():
    Top15 = one()
    ratio = Top15['Self-citations'] / Top15['Citations']
    Top15['ratio'] = ratio
    maxRatio = (Top15['ratio'].max())
    return (Top15[Top15['ratio'] == maxRatio].index[0],maxRatio)



def eight():
    Top15 = one()
    Top15['POPEstimate'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    nlargest = Top15.nlargest(3,'POPEstimate')
    return nlargest.iloc[2].name


def nine():
    Top15 = one()
    Top15['POPEstimate'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['POPEstimate']
    return Top15.corr(method="pearson")['Energy Supply per Capita']['Citable docs per Capita']




def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])




def ten():
    Top15 = one()
    med = Top15['% Renewable'].median()
       
    Top15['HighRenew'] = [1 if x >= med else 0 for x in Top15['% Renewable']]  
    ans = Top15['HighRenew']    
    return pd.Series(ans)




def eleven():
    ContinentDict  = {'China':'Asia', 
                          'United States':'North America', 
                          'Japan':'Asia', 
                          'United Kingdom':'Europe', 
                          'Russian Federation':'Europe', 
                          'Canada':'North America', 
                          'Germany':'Europe', 
                          'India':'Asia',
                          'France':'Europe', 
                          'South Korea':'Asia', 
                          'Italy':'Europe', 
                          'Spain':'Europe', 
                          'Iran':'Asia',
                          'Australia':'Australia', 
                          'Brazil':'South America'}
    Top15 = one()
    Top15['POPEstimate'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Continent'] = [ContinentDict[Country] for Country in Top15.index]
    Top15 = Top15.reset_index()
    Top15.set_index('Continent',inplace=True)
    df = Top15.groupby(level=0)['POPEstimate'].agg({'mean':np.mean,
                                                               'std':np.std,
                                                               'sum':np.sum,
                                                               'size':np.size})
    print(df)
    return df

eleven()



def twelve():
    Top15 = one()
    ContinentDict  = {'China':'Asia', 
                      'United States':'North America', 
                      'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}
    Top15['Continent'] = [ContinentDict[Country] for Country in Top15.index]
    Top15.reset_index(inplace=True)
    Top15['bins'] = pd.cut(Top15['% Renewable'],5)
    df = Top15.groupby(['Continent','bins']).size()
    return df




def thirteen():
    Top15 = one()
    Top15['POPEstimate'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    PopEst = Top15.POPEstimate
    tmp = PopEst.tolist()
    PopEst = PopEst.apply(lambda x: '{0:,}'.format(x),tmp)
    PopEst.rename('PopEst',inplace=True)
    return PopEst



def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")

