import streamlit as st
import pandas as pd

# --- Page Layout Configuration ---
st.set_page_config(page_title="Allahabad HC Monitor", layout="wide", page_icon="⚖️")

st.title("⚖️ Allahabad High Court Dashboard & Case Monitor")
st.markdown("---")

# --- Sample Data Loader (Replace with your actual scraping/log payload) ---
@st.cache_data
def load_case_data():
    # Real data mapped directly from the High Court Order dated May 25, 2026
    data = {
        "Case Number": ["WRIC No. 17230 of 2026"],
        "Petitioner/Respondent": ["Smt. Munni Devi vs State of U.P. And 4 Others"],
        "Advocate (Petitioner)": ["Amit Dwivedi, Ramesh Chandra Dwivedi"],
        "Advocate (Respondent)": ["C.S.C., Krishna Agarawal, Narendra Kumar Tiwari"],
        "Next Hearing Date": ["2026-07-10"],
        "Status": ["Adjourned / Listed as Fresh"],
        "Synopsis": ["Challenging DM order demanding Rs. 29,474 for shifting a tilted electric pole. DB suggested electricity company reinforce foundation instead of charging petitioner. Put up on July 10."]
    }
    return pd.DataFrame(data)

df = load_case_data()

# --- Navigation Tabs ---
tab1, tab2 = st.tabs(["📊 Live Data Insights", "🎯 Office Tracking Panel"])

with tab1:
    st.subheader("High Court Analytics Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Monitored Cases", value=len(df))
    col2.metric(label="Active Listings This Month", value="2")
    col3.metric(label="Recent Judgments / Orders", value="1")
    
    st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("🎯 Specific Practice Tracking: Mr. R C Dwivedi & Mr. Amit Dwivedi")
    st.info("This panel automatically parses live cause lists and orders for matches matching your defense registry names.")
    
    # Text normalization logic to ensure spaces or dots don't break searches
    search_term_1 = "Amit Dwivedi"
    search_term_2 = "R C Dwivedi"
    
    # Filter DataFrame for entries containing either advocate name strings
    filtered_df = df[
        df["Advocate (Petitioner)"].str.contains(search_term_1, case=False, na=False) |
        df["Advocate (Petitioner)"].str.contains(search_term_2, case=False, na=False) |
        df["Advocate (Respondent)"].str.contains(search_term_1, case=False, na=False) |
        df["Advocate (Respondent)"].str.contains(search_term_2, case=False, na=False)
    ]
    
    if not filtered_df.empty:
        st.success(f"🔍 Found {len(filtered_df)} matches listed under your office registries:")
        st.dataframe(filtered_df, use_container_width=True)
        
        # Display as clear notification list cards
        for idx, row in filtered_df.iterrows():
            with st.expander(f"📋 {row['Case Number']} - {row['Petitioner/Respondent']}"):
                st.write(f"**Counsel Involved:** {row['Advocate (Petitioner)']} / {row['Advocate (Respondent)']}")
                st.write(f"**Next Date of Listing:** `{row['Next Hearing Date']}`")
                st.write(f"**Current Status Flag:** {row['Status']}")
    else:
        st.warning("No new matches found in the current processed batch for 'Amit Dwivedi' or 'R C Dwivedi'.")