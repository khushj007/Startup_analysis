import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", )
st.sidebar.title("Startup Funding Analysis")
options = st.sidebar.selectbox("Select", ["Overall Analysis", "Startup", "Investor"])
df = pd.read_csv("startup.csv")
investors = sorted(set(df["investors"].str.split(",").sum()))[2:]
startup = df["startup"].values
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month



def about_investor(investor):
    temp_df = df[df["investors"].str.contains(investor)]

    st.header(investor)
    investor_df = temp_df.head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.header("Recent Investment")
    st.dataframe(investor_df)
    biggest_df = df[df["investors"].str.contains(investor)].groupby("startup").agg({"amount": "sum"
                                                                                    }).sort_values("amount",

                                                                                                   ascending=False).head()

    gi_sector = temp_df.groupby("vertical")["amount"].sum()
    stage_sector = temp_df.groupby("round")["amount"].sum()
    city = temp_df.groupby("city")["amount"].sum()
    col1, col2 = st.columns(2)
    with col1:
        st.header("Biggest Investment")
        st.bar_chart(biggest_df)
    with col2:
        st.header("Sectorwise Investment")
        fig, ax = plt.subplots()
        ax.pie(gi_sector.values, labels=gi_sector.index, autopct='%1.1f%%')
        st.pyplot(fig)
    col1, col2 = st.columns(2)
    with col1:
        st.header("Stagewise Investment")
        fig1, ax1 = plt.subplots()
        ax1.pie(stage_sector.values, labels=stage_sector.index, autopct='%1.1f%%')
        st.pyplot(fig1)

    with col2:
        st.header("Citywise Investment")
        fig2, ax2 = plt.subplots()
        ax2.pie(city.values, labels=city.index, autopct='%1.1f%%')
        st.pyplot(fig2)

    st.header("YOY Investment")
    yoy_result = temp_df.groupby("year").agg({
        "amount": "sum"
    })
    fig3, ax3 = plt.subplots()
    ax3.plot(yoy_result.index, yoy_result.values)
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Amount in crore')

    st.pyplot(fig3)


def overall_analysis():
    total = str(round(df["amount"].sum())) + " Cr"
    max_amt = df.groupby("startup")["amount"].sum().sort_values(ascending=False).head(1).values[0]
    avg_amt = round(df["amount"].mean())
    total_funded = df["startup"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Investment", total)
    with col2:
        st.metric("Max Investment", str(max_amt) + " Cr")
    with col3:
        st.metric("Avg Investment", str(avg_amt) + " Cr")
    with col4:
        st.metric("Total Funded startups", total_funded)

    st.header("MOM investment")
    y_axis = st.selectbox("select Y axis", ["investment amount", "No.o of startup funded"])
    if y_axis == "investment amount":
        result = df.groupby(["year", "month"])["amount"].sum().reset_index()
        result["year-month"] = result["month"].astype(str) + result["year"].astype(str)
        fig, ax = plt.subplots()
        ax.plot(result["year-month"].values, result["amount"].values)
        ax.set_xlabel("TimeLine")
        ax.set_ylabel(y_axis)
        st.pyplot(fig)

    else:
        result = df.groupby(["year", "month"])["startup"].count().reset_index()
        result["year-month"] = result["month"].astype(str) + result["year"].astype(str)
        fig1, ax1 = plt.subplots()
        ax1.plot(result["year-month"].values, result["startup"].values)
        ax1.set_xlabel("TimeLine")
        ax1.set_ylabel(y_axis)
        st.pyplot(fig1)


if options == "Overall Analysis":
    st.title(options)
    overall_analysis()
elif options == "Startup":
    st.title(options)
    startup = st.sidebar.selectbox("Startup", startup)
else:
    st.title(options)
    investor = st.sidebar.selectbox("Investors", investors)
    btn = st.sidebar.button("Find")
    if btn:
        about_investor(investor)
