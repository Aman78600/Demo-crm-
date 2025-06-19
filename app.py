import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    excel_file = pd.ExcelFile("crm_test_case_data.xlsx")
    companies = excel_file.parse('Companies')
    people = excel_file.parse('People')
    return companies, people

companies_df, people_df = load_data()

# Merge to associate people with company info
merged_df = people_df.merge(companies_df, left_on="Company", right_on="Company Name", how="left")

# Sidebar Navigation
st.sidebar.title("Simple CRM Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Companies", "People", "Leads"])

# Dashboard Page
if page == "Dashboard":
    st.title("📊 CRM Dashboard Overview")
    st.metric("Total Companies", len(companies_df))
    st.metric("Total People", len(people_df))
    top_industries = companies_df['Industry'].value_counts().head(5)
    st.subheader("Top Industries")
    st.bar_chart(top_industries)

# Companies Page
elif page == "Companies":
    st.title("🏢 Companies")
    industry_filter = st.selectbox("Filter by Industry", ["All"] + sorted(companies_df['Industry'].unique().tolist()))
    if industry_filter != "All":
        filtered = companies_df[companies_df['Industry'] == industry_filter]
    else:
        filtered = companies_df
    st.dataframe(filtered)

# People Page
elif page == "People":
    st.title("🧑 Contacts")
    company_filter = st.selectbox("Filter by Company", ["All"] + sorted(people_df['Company'].unique().tolist()))
    if company_filter != "All":
        filtered = people_df[people_df['Company'] == company_filter]
    else:
        filtered = people_df
    st.dataframe(filtered)

# Leads Page
elif page == "Leads":
    st.title("🗂️ Lead Management")

    # Simulated Lead Status (store in session_state for demo)
    if "lead_status" not in st.session_state:
        st.session_state.lead_status = {name: "New" for name in people_df['Name']}

    for i, row in people_df.iterrows():
        name = row['Name']
        col1, col2, col3 = st.columns([3, 2, 2])
        col1.markdown(f"**{name}** - {row['Company']}")
        current_status = st.session_state.lead_status.get(name, "New")
        new_status = col2.selectbox("Status", ["New", "Contacted", "Qualified", "Converted", "Lost"],
                                    key=f"status_{i}", index=["New", "Contacted", "Qualified", "Converted", "Lost"].index(current_status))
        if new_status != current_status:
            st.session_state.lead_status[name] = new_status
        col3.markdown(f"**Status**: {st.session_state.lead_status[name]}")
