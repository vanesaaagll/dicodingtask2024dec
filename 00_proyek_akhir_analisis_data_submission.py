# Kriteria 1: Menggunakan Salah Satu dari Dataset yang Telah Disediakan
## Bike Sharing Dataset (Sumber)

# Kriteria 2: Melakukan Seluruh Proses Analisis Data
## Membuat 2 pertanyaan:
# Pertanyaan #1 : How many total of users (including registered and casual user) within a range of dates? 
# Pertanyaan #2 : What is the total number of users based on season, hours spent, and weather situation?
# Pertanyaan #3 : What are the average values of temperature, humidity, and windspeed conditions?

# Import the Library :
import pandas as pd
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# DATA WRANGLING
# Gathering the Data by read and load the csv dataset
day_df = pd.read_csv("./Bike-sharing-dataset/day.csv")
# print(day_df.head(5))
hour_df = pd.read_csv("./Bike-sharing-dataset/hour.csv")
#   print(hour_df.head(5))

# Assessing Data
# Check missing value and duplicate
# print(day_df.info()) # show table info
# print(day_df.describe()) # show table mean, std, etc
# print(day_df.isna().sum())
# print(day_df.duplicated().sum())
# print(hour_df.isna().sum())
# print(hour_df.duplicated().sum())

# Cleaning Data:
# There is no duplicate and missing value
# Change the value from normalized temp into Celcius by multiplying with 41
day_df["temp"]=day_df["temp"]*41
# Change the value from normalized humidity into percentage by multiplying with 100
day_df["hum"]=day_df["hum"]*100
# Change the value from normalized windspeed into km/h by multiplying with 67
day_df["windspeed"]=day_df["windspeed"]*67
# Mapping the season into their name
day_df["season"]=day_df["season"].map({
    1:"springer",
    2:"summer",
    3:"fall", 
    4:"winter"
})
hour_df["season"]=hour_df["season"].map({
    1:"springer",
    2:"summer",
    3:"fall", 
    4:"winter"
})
# print(day_df["season"].head(26))
day_df["weathersit"]=day_df["weathersit"].map({
    1: "Clear, Few clouds, Partly cloudy, Partly cloudy",
	2: "Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist",
	3: "Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds",
	4: "Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog"
})
hour_df["weathersit"]=hour_df["weathersit"].map({
    1: "Clear, Few clouds, Partly cloudy, Partly cloudy",
	2: "Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist",
	3: "Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds",
	4: "Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog"
})


# EXPLORATORY DATA
# Pertanyaan #1 : How many total of users (including registered and casual user) within a range of dates? 
# Pertanyaan #2 : What is the total number of users based on season, hours spent, and weather situation?
# Pertanyaan #3 : What are the average values of temperature, humidity, and windspeed conditions?

# Pertanyaan #1 : How many total of users (including registered and casual user) within a range of dates?
# # Sum season
# sum_season = day_df.groupby("season").cnt.sum().sort_values(ascending=False).reset_index()
# print(sum_season)
# sum_season_hour = hour_df.groupby("season").hr.sum().sort_values(ascending=False).reset_index()
# # Most Rented Season
# max_season = sum_season.loc[sum_season["cnt"].idxmax()] # index max
# max_season_name = max_season["season"]
# max_season_total_user = max_season["cnt"]
# print(f"The most used bike counted by user is in : {max_season_name} with total of user {max_season_total_user}")
# # Least Rented Season
# min_season = sum_season.loc[sum_season["cnt"].idxmin()] # index max
# min_season_name = min_season["season"]
# min_season_total_user = min_season["cnt"]
# print(f"The least used bike counted by user is in : {min_season_name} with total of user {min_season_total_user}")


# DASHBOARD
# Pertanyaan #1 : How many total of users (including registered and casual user) within a range of dates? 
# Show filter date range in widget date input 
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
with st.sidebar:
    st.image("https://global-uploads.webflow.com/57822c659e1627a433e6a7c6/5e412802e8a6bf79ebff0083_Bike%20Rental.png")
    start_date, end_date = st.date_input(
        label="📅 Select the date range here", min_value=min_date,max_value=max_date, value=[min_date,max_date]
    )

# Filter by date range
filtered_day_df = day_df[(day_df["dteday"]>=str(start_date)) &
                 (day_df["dteday"]<=str(end_date))]
filtered_hour_df = hour_df[(hour_df["dteday"]>=str(start_date)) & (hour_df["dteday"]<=str(end_date))]

# Title of the Dashboard:
st.header("Bike Rent Dataset Monitoring & Insights🚴‍♀️✨")

# Total Users
total_users = filtered_day_df.cnt.sum()
st.metric("Total Users of Bikes Rented", value=f"{total_users:,}")

# Show the total users that registered and usual
st.subheader("Users Type")
col1, col2 = st.columns(2)
with col1:
    casual_user = filtered_day_df["casual"].sum()
    st.metric("Casual Users", value=f"{casual_user:,}")
with col2:
    registered_user = filtered_day_df["registered"].sum()
    st.metric("Registered Users", value=f"{registered_user:,}")

fig, ax = plt.subplots(figsize=(20,10))
ax.plot(
    filtered_day_df["dteday"],
    filtered_day_df["cnt"],
    marker ="o",
    linewidth=2,
    color="#90CAF9"
)
# Set Title
ax.set_title("Total Users per Date", fontsize=24, fontweight="bold")
# Adjust the axis size
ax.tick_params(axis="y",labelsize=20)
ax.tick_params(axis="x",labelsize=15)
st.pyplot(fig)


# Pertanyaan #2 : What is the total number of users based on season, hours spent, and weather situation?
# Visualize the total of Users in every season
st.subheader("Total of Users and Hours per Season")
filtered_sum_season = filtered_day_df.groupby("season").cnt.sum().sort_values(ascending=False).reset_index()
fig, ax=plt.subplots(nrows=1, ncols=2, figsize=(35,15)) 
color_user = ["#8B1A1A", "#FFD6D1", "#FFD6D1", "#FFD6D1"]
sns.barplot(x="cnt", y="season", data=filtered_sum_season, palette=color_user, ax=ax[0])  
ax[0].set_ylabel("Season", fontsize=30)
ax[0].set_xlabel("#Users", fontsize=30)
ax[0].set_title("Total Users", loc="center", fontsize=50)
ax[0].tick_params(axis="y", labelsize=35)
ax[0].tick_params(axis="x",labelsize=30)    
ax[0].xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))  # Format with commas

# Visualize the total of Hours Spent in every season
filtered_sum_season_hour = filtered_hour_df.groupby("season").hr.sum().sort_values(ascending=False).reset_index()
sns.barplot(x="hr", y="season", data=filtered_sum_season_hour, palette=color_user, ax=ax[1])
ax[1].set_ylabel("Season", fontsize=30)
ax[1].set_xlabel("#Hours", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Total Hours", loc="center", fontsize=50)
ax[1].tick_params(axis="y", labelsize=35)
ax[1].tick_params(axis="x",labelsize=30) 
ax[1].xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))  # Format with commas
st.pyplot(fig)

# Visualize the total of Hours Spent by Weather Situation
st.subheader("Total Users Categorized by Weather Situation")
byweathersit_df = filtered_hour_df.groupby("weathersit").cnt.sum().reset_index()
print(byweathersit_df)

plt.figure(figsize=(10,5))
sns.barplot(
    y="cnt",
    x="weathersit",
    data=byweathersit_df,
    palette="pastel"
)
plt.title("Total Users by Weather Situation", loc="center", fontsize=15)
plt.ylabel("Total Users")
plt.xlabel("Weather Situation")
plt.tick_params(axis="x", labelsize=12)
plt.tick_params(axis="y", labelsize=12)
plt.gca().yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))  # Format with commas

# Add legend instead of x-axis labels
weather_labels = byweathersit_df["weathersit"].unique()
handles = [plt.Rectangle((0,0),1,1, color=sns.color_palette("pastel")[i]) for i in range(len(weather_labels))]
plt.legend(handles, weather_labels, title="Weather Situation", bbox_to_anchor=(1.05, 1), loc='upper left')
# Remove x-axis labels
plt.gca().set_xticklabels([])
st.pyplot(plt)


# Pertanyaan #3 : What are the average values of temperature, humidity, and windspeed conditions?
# Show the average temperature, humidity, and windspeed
st.subheader("Average")
col3, col4, col5 = st.columns(3)
with col3:
    average_temp = filtered_day_df["temp"].mean().round(1)
    st.metric("Average Temperature (in Celcius)", value=f"{average_temp:,}")
with col4:
    average_hum = filtered_day_df["hum"].mean().round(1)
    st.metric("Average Humidity", value=f"{average_hum:,}")
with col5:
    windspeed = filtered_day_df["windspeed"].mean().round(1)
    st.metric("Average Windspeed", value=f"{windspeed:,}")
