import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

# Load Excel data
@st.cache_data
def load_data():
    xl = pd.ExcelFile("crm_test_case_data.xlsx")
    companies = xl.parse("Companies")
    people = xl.parse("People")
    return companies, people

# Load data
companies_df, people_df = load_data()

# Simulate lead statuses (if not already present)
if "Lead Status" not in people_df.columns:
    people_df["Lead Status"] = [random.choice(["New", "Contacted", "Qualified", "Converted", "Lost"])
                                for _ in range(len(people_df))]

# Set up sidebar navigation
st.sidebar.title("CRM Navigation")
page = st.sidebar.radio("Go to", ["📊 Dashboard", "🏢 Companies", "🧑 People", "📂 Leads"])

# ------------------ PAGE: DASHBOARD ------------------
if page == "📊 Dashboard":
    st.title("📊 CRM Dashboard")

    # Top KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Companies", len(companies_df))
    col2.metric("Total Contacts", len(people_df))
    col3.metric("Total Revenue (M)", f"${companies_df['Revenue (in Millions)'].sum():,.2f}")
    col4.metric("Industries", companies_df['Industry'].nunique())

    st.divider()

    # Chart: Companies per Industry
    st.subheader("🏭 Companies per Industry")
    industry_counts = companies_df['Industry'].value_counts()
    st.bar_chart(industry_counts)

    # Chart: Lead Status Pie Chart
    st.subheader("🧭 Lead Status Distribution")
    status_counts = people_df['Lead Status'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    # Top companies
    st.subheader("💼 Top 5 Companies by Revenue")
    top_rev = companies_df.sort_values(by="Revenue (in Millions)", ascending=False).head(5)
    st.table(top_rev[['Company Name', 'Revenue (in Millions)', 'Industry']])

    # Top contacts
    st.subheader("🧑 Top 10 Contacts")
    st.table(people_df[['Name', 'Email', 'Title', 'Company']].head(10))

# ------------------ PAGE: COMPANIES ------------------
elif page == "🏢 Companies":
    st.title("🏢 Companies")
    industry_filter = st.selectbox("Filter by Industry", ["All"] + sorted(companies_df['Industry'].unique().tolist()))
    filtered = companies_df if industry_filter == "All" else companies_df[companies_df['Industry'] == industry_filter]
    st.dataframe(filtered)

# ------------------ PAGE: PEOPLE ------------------
elif page == "🧑 People":
    st.title("🧑 Contacts")
    company_filter = st.selectbox("Filter by Company", ["All"] + sorted(people_df['Company'].unique().tolist()))
    filtered = people_df if company_filter == "All" else people_df[people_df['Company'] == company_filter]
    st.dataframe(filtered[['Name', 'Email', 'Phone Number', 'Title', 'Company']])

# ------------------ PAGE: LEADS ------------------
elif page == "📂 Leads":
    st.title("📂 Lead Management")

    # Track lead status updates
    if "lead_status" not in st.session_state:
        st.session_state.lead_status = {row['Name']: row['Lead Status'] for _, row in people_df.iterrows()}

    for i, row in people_df.iterrows():
        name = row["Name"]
        with st.expander(f"{name} - {row['Company']}"):
            col1, col2 = st.columns([3, 2])
            new_status = col1.selectbox(
                "Update Lead Status",
                ["New", "Contacted", "Qualified", "Converted", "Lost"],
                index=["New", "Contacted", "Qualified", "Converted", "Lost"].index(
                    st.session_state.lead_status[name]
                ),
                key=f"status_{i}"
            )
            st.session_state.lead_status[name] = new_status
            col2.write(f"📌 Current: **{st.session_state.lead_status[name]}**")
