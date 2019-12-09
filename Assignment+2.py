import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()

def zero():
    return df.loc['Afghanistan']



def one():
    return df[df.Gold == df.Gold.max()].index[0]




def two():
    return (df['Gold'] - df['Gold.1']).argmax()


def three():
    winners = df[(df['Gold'] > 0) & (df['Gold.1'] > 0)]
    return ((winners['Gold'] - winners['Gold.1']).abs() / winners['Gold.2']).argmax()


def four():
    weightedCounts = df.apply(lambda country : country['Gold.2'] * 3 + country['Silver.2'] * 2 + country['Bronze.2'] * 1 ,axis=1)
    return weightedCounts


census_df = pd.read_csv('census.csv')
census_df.head()



def five():
    return census_df[census_df.SUMLEV == 50].STNAME.value_counts().idxmax()


def six():
    counties = census_df[census_df['SUMLEV'] == 50]
    top_threes = counties.groupby('STNAME')['CENSUS2010POP'].nlargest(3)
    states = top_threes.groupby(level=0).sum()
    return [states.nlargest(3).index[0],states.nlargest(3).index[1],states.nlargest(3).index[2]]



population_estimates = ["POPESTIMATE2010",
			    "POPESTIMATE2011",
			    "POPESTIMATE2012",
			    "POPESTIMATE2013",
			    "POPESTIMATE2014",
			    "POPESTIMATE2015"]
def seven():
    counties = census_df[census_df['SUMLEV'] == 50]
    return(counties.loc[(counties[population_estimates].max(axis=1) - counties[population_estimates].min(axis=1)).argmax()].CTYNAME)


def eight():
    counties = census_df[census_df['SUMLEV'] == 50]
    countiesWithRegion = counties.loc[(counties.REGION == 2) | (counties.REGION == 1)]
    countiesWithWashington = countiesWithRegion[countiesWithRegion.CTYNAME.str.startswith('Washington')]
    countiesWithGreaterPop = countiesWithWashington[countiesWithWashington['POPESTIMATE2015'] > countiesWithWashington['POPESTIMATE2014']]
    return countiesWithGreaterPop[['STNAME','CTYNAME']].sort_index()