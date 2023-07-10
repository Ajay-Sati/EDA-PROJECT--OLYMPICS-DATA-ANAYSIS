
import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from plotly.figure_factory import create_distplot
import scipy
from PIL import Image

df= pd.read_csv('athlete_events.csv')
region_df= pd.read_csv('noc_regions.csv')

df= preprocessor.preprocess(df,region_df)
st.sidebar.title('OLYMPICS ANALYSIS.')
user_input= st.sidebar.radio(
    "SELECT AN OPTION",
    ("Olympics alaysis","Medal Tally(Country Wise)","Medal Tally(Year Wise)","Overall Analysis","Country-Wise Analysis","Athletes  Wise Analysis")
)

if user_input== "Olympics alaysis":
    st.header("OLYMPICS ANALYSIS.")
    st.divider()
    image=Image.open("olympics.jpg")
    st.image(image)



if user_input == 'Medal Tally(Country Wise)':
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    years,country = helper.country_year_list(df)

    selected_country = st.sidebar.selectbox("Select Country", country)
    if selected_country=="Overall":
        medal_df = medal_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                              ascending=False).reset_index()

        medal_df['total'] = medal_df['Gold'] + medal_df['Silver'] +medal_df['Bronze']
        medal_df['Gold'] = medal_df['Gold'].astype('int')
        medal_df['Silver'] = medal_df['Silver'].astype('int')
        medal_df['Bronze'] = medal_df['Bronze'].astype('int')
        medal_df['total'] = medal_df['total'].astype('int')
        st.header("Overall Medal Tally")

    else:
        medal_df= medal_df[medal_df['region']==selected_country]
        medal_df = medal_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()

        medal_df['total'] = medal_df['Gold'] + medal_df['Silver'] + medal_df['Bronze']
        medal_df['Gold'] = medal_df['Gold'].astype('int')
        medal_df['Silver'] = medal_df['Silver'].astype('int')
        medal_df['Bronze'] = medal_df['Bronze'].astype('int')
        medal_df['total'] = medal_df['total'].astype('int')
        medal_df['Year'] = medal_df['Year'].astype('string')
        st.header("Medal Tally for"+' '+selected_country)

    st.dataframe(medal_df)





if user_input == 'Medal Tally(Year Wise)':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,year=selected_year,country=selected_country)

    if selected_year != 'Overall' and selected_country == 'Overall':
        st.header("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.header(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)


if user_input=="Overall Analysis":
    editions= df['Year'].nunique()-1
    cities= df['City'].nunique()
    sports= df["Sport"].nunique()
    events= df['Event'].nunique()
    athletes= df["Name"].nunique()
    nation=  df["region"].dropna().nunique()


    st.title("Top Statistics. ")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.title("Editions.")
        st.subheader(editions)

    with col2:
        st.title("Host Cities.")
        st.subheader(cities)

    with col3:
        st.title("Sports.")
        st.subheader(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.title("Events.")
        st.subheader(events)

    with col2:
        st.title("Athletes.")
        st.subheader(athletes)

    with col3:
        st.title("Nations.")
        st.subheader(nation)


    countries_over_time= helper.number_of_countries_over_time(df)
    st.title("PARTICIPATING NATIONS OVER TIME.")
    fig = px.line(countries_over_time, x="Year", y="Number of Countries")
    st.plotly_chart(fig)


    events_over_time= helper.number_of_events_over_time(df)
    st.title("EVENTS OVER TIME.")
    fig = px.bar(events_over_time, x='Year', y="Number of Events")
    st.plotly_chart(fig)


    atheletes_over_time=helper.number_of_athelets_over_time(df)
    st.title("PARTICIPATING ATHLETES OVER TIME.")
    fig = px.line(atheletes_over_time, x="Year", y="Number of Atheletes")
    st.plotly_chart(fig)



    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True,annot_kws={"size":9})
    st.pyplot(fig )

    sports = df["Sport"].unique().tolist()
    sports.sort()
    sports.insert(0, "Overall")
    selected_sports =st.selectbox("Select type of sports.",sports)
    st.title("Most successfull Athletes"+"("+selected_sports+")")
    success = helper.most_successfull(df,selected_sports)
    st.table(success)


if user_input=="Country-Wise Analysis":
    st.title("COUNTRY WISE ANALYSIS.")
    country=st.sidebar.selectbox("SELECT AN OPTION.",df["region"].dropna().unique())
    st.subheader("Medal tally for"+" "+ country)
    medal_tally,medaltally1= helper.country_wise_medal_tally(df, country)
    st.table(medal_tally)


    st.subheader("Total Count Of Medal Over Year.")
    fig=px.line(medaltally1, x="Year", y="Total")
    st.plotly_chart(fig)



    st.subheader(country+"Excel in sports")
    temp_df = df.dropna(subset=["Medal"])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    temp_df = temp_df[temp_df["region"] == country]
    fig, ax = plt.subplots(figsize=(8,8))
    ax=sns.heatmap(temp_df.pivot_table(index="Sport",columns="Year", values="Medal", aggfunc="count").fillna(0).astype(int),annot=True,annot_kws={"size":9})
    st.pyplot(fig)


    st.subheader("Best Athlete  of "+country)
    list_sports= helper.sports_played(df,country)
    selected_sport=st.selectbox("Select Sport",list_sports)
    best_atheletes= helper.most_success_atheletes(df,country,selected_sport)

    st.table(best_atheletes)


if user_input=="Athletes  Wise Analysis":
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    x1 = athlete_df["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x4 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4],
                             ["Overall Analysis", "Gold Medalist", "Silver Medalist", "Bronze Medalist"],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=500 )
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    st.title("Details of your favourite athletes.")
    name = st.selectbox("Select Name of athelte", df["Name"].unique().tolist())
    data = helper.fav_athletes_details(df, name)
    st.table(data)


