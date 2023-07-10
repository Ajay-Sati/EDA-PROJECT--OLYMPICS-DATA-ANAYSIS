import pandas as pd


def fetch_medal_tally(df, year, country):
    temp_df = None
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
        flag = 1
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == year]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def medal_tally(df):
    medal_tally = df.drop_duplicates(['Team', "NOC", "Games", "Year", "City", "Sport", "Event", "Medal"])
    medal_tally = medal_tally.groupby("region").sum()[['Gold', "Silver", "Bronze"]].sort_values("Gold",
                                                                                                ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally["Silver"] + medal_tally["Bronze"]
    medal_tally = pd.concat([medal_tally['region'], medal_tally[["Gold", "Silver", "Bronze", 'Total']].astype(int)],
                            axis=1)

    return (medal_tally)


def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()

    country = df['region'].unique().tolist()
    country.insert(0, "Overall")

    return (year, country)


def number_of_countries_over_time(df):
    year = df[["Year", "region"]].drop_duplicates()
    year = year.groupby("Year")["region"].count().reset_index()
    year.rename(columns={"region": "Number of Countries"}, inplace=True)
    return (year)


def number_of_events_over_time(df):
    Event = df[["Year", "Event"]].drop_duplicates()
    Event = Event.groupby("Year")["Event"].count().reset_index()
    Event.rename(columns={"Event": "Number of Events"}, inplace=True)
    return (Event)


def number_of_athelets_over_time(df):
    Atheletes = df[["Year", "Name"]].drop_duplicates()
    Atheletes = Atheletes.groupby("Year")["Name"].count().reset_index()
    Atheletes.rename(columns={"Name": "Number of Atheletes"}, inplace=True)
    return (Atheletes)


def most_successfull(df, sport):
    temp_df = df.dropna(subset=["Medal"])

    if sport != "Overall":
        temp_df = temp_df[temp_df["Sport"] == sport]

    x = temp_df["Name"].value_counts().reset_index().head(10).merge(df, left_on="Name", right_on="Name", how="left")[
        ["Name", "count", "Sport", "region"]].drop_duplicates()

    return (x)


def country_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    temp_df = temp_df[temp_df["region"] == country]
    temp_df = temp_df.groupby("Year")[["Gold", "Silver", "Bronze"]].sum().reset_index()
    total_df = temp_df.copy()
    total_df["Total"] = temp_df["Gold"] + temp_df["Silver"] + temp_df["Bronze"]
    return temp_df, total_df


def sports_played(df, country):
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df = temp_df[temp_df["region"] == country]
    sports = temp_df["Sport"].unique().tolist()
    sports.sort()
    sports.insert(0, 'Overall')
    return sports


def most_success_atheletes(df, country, sport):
    temp_df = df.dropna(subset=["Medal"])

    if sport == "Overall":
        temp_df = temp_df[temp_df["region"] == country]
        x = \
        temp_df["Name"].value_counts().reset_index().head(10).merge(df, left_on="Name", right_on="Name", how="left")[
            ["Name", "count", "Sport", "region"]].drop_duplicates()

    if sport != "Overall":
        temp_df = temp_df[(temp_df["region"] == country) & (temp_df["Sport"] == sport)]
        x = temp_df["Name"].value_counts().reset_index().head(10)

    return (x)


def fav_athletes_details(df, name):
    temp_df = df[df["Name"] == name]
    x = temp_df.groupby("Year")["Medal"].count()
    return (x)

    