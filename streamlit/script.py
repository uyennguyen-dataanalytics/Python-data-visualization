import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Adding title and short description for the dashboard
st.title("A&E Waiting Times Dashboard")
st.write("An overview of patient waiting times at Accident & Emergency (A&E) department")

@st.cache_data
def load_data():
    """Read .csv file named "ae_visits.csv" and return it as DataFrame"""
    return pd.read_csv("ae_visits.csv")

# Call function and store DataFrame in variable "visits"
visits = load_data()

# Display DataFrame "visists" as an interactive table
st.dataframe(visits)

# Calculate the key figures for the dashboard
def key_figures(df):
    """Calculate key figures for the dashboard"""
    total_visits = len(df)
    average_wait = df['wait_minutes'].mean()
    percentage_admitted = (df['outcome'] == "Admitted").mean()*100
    percentage_wait = (df['wait_minutes'] <= 240).mean()*100
    return (total_visits, average_wait, percentage_admitted, percentage_wait)

# Call function and store values in variable "key"
key = key_figures(visits)

# Add sidebar
st.sidebar.header("Filters")

# Add control to choose triage category
triage_option = st.sidebar.multiselect("Triage category", options=[1,2,3,4,5], default=[1,2,3,4,5])

# Add drop-down list for age group
age_option = st.sidebar.selectbox("Age group", options=["All", "0-17", "18-39", "40-64", "65+"])

# Create DataFrame "filtered"
filtered = visits[visits["triage_category"].isin(triage_option)]

if age_option != "All":
    filtered = filtered[filtered["age_group"] == age_option]

if filtered.empty:
    st.warning("No visits match the filters")
    st.stop()

# Create a histogram showing distribution of waiting times
def wait_histogram(df):
    """Create a histogram showing distribution of waiting times, with a vertical line marking 4-hour target"""
    fig1, ax1 = plt.subplots()
    ax1.hist(df["wait_minutes"], bins=range(0,361,30), edgecolor="black")
    ax1.axvline(x=240, ls="--", label="4-hour target", color="red")
    ax1.set_title("Distribution of patient waiting times")
    ax1.set_xlabel("Waiting time (minute)")
    ax1.set_ylabel("Number of patients")
    ax1.legend()
    return fig1

# Create a bar chart showing the average waiting times for each triage category
def wait_bar_chart(df):
    """Create a bar chart showing the average waiting times for each triage category"""
    fig2, ax2 = plt.subplots()
    average = df.groupby("triage_category")["wait_minutes"].mean()
    ax2.bar(average.index, average.values)
    ax2.set_title("Average wait by triage category")
    ax2.set_xlabel("Triage category")
    ax2.set_ylabel("Average wait (minutes)")
    ax2.set_xticks([1, 2, 3, 4, 5])
    return fig2

# Create layout for the dashboard and button for dowwnloading data
tab1, tab2, tab3 = st.tabs(["Overview", "Waiting times", "Data"])

# Fill tab 'Overview" with the key metrics: Total visits, Average wait, Admitted, Seen within 4 hours
# and the charts showing visits per day and visits by arrival hour 
with tab1:
    key = key_figures(filtered)
    
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Total visits", value=key[0])
        col2.metric(label="Average wait", value=f"{key[1]:.1f} min")
        col3.metric(label="Admitted", value=f"{key[2]:.1f}%")
        col4.metric(label="Seen within 4 hours", value=f"{key[3]:.1f}%")
    
    st.subheader("Visits per day")
    visits_per_day = (filtered.groupby("date").size().reset_index(name="visits_per_day"))
    st.line_chart(visits_per_day, x="date", y="visits_per_day", x_label="Date", y_label="Number of visits")

    st.subheader("Visits by arrival hour")
    visits_per_hour = (filtered.groupby("arrival_hour").size().reset_index(name="visits_per_hour"))
    st.bar_chart(visits_per_hour, x="arrival_hour", y="visits_per_hour", x_label="Arrival hour", y_label="Number of visits")

# Fill tab "Waiting times" with histogram and bar chart displaying waiting times between groups
with tab2:
    st.subheader("Distribution of patient waiting times")
    st.pyplot(wait_histogram(filtered))

    st.subheader("Average wait by triage category")
    st.pyplot(wait_bar_chart(filtered))

# Fill tab "Data" with button for download, information about dataset and explanation about triage category and 4-hour target in England
with tab3:
    st.download_button("Download", data=filtered.to_csv(index=False), file_name="filtered_visits.csv", mime="text/csv")
    with st.expander("About this data"):
        st.write("""
                **Triage category**\n
                The category indicates the urgency of patient's condition, ranging from 1 (most urgent) to 5 (least urgent).\n
                **4-hour target**\n
                Hospitals in England aim to admit, transfer or discharge A&E patients within 4 hours of arrival.
                """)
